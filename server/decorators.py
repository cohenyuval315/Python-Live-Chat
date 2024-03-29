import typing
from typing import Dict,Any
from aiohttp import web
from constants import StatusCodes,Errors,BlockType,RoleType
from exceptions import InternalServerError,AlreadyExistsError,DoesNotExistsError
from utils import create_response
import datetime
from logger import logger
from sqlalchemy.exc import SQLAlchemyError


def exception_handler():
    def deco(func):
        async def inner(cls, request: web.Request, *args, **kwargs):
            try:
                return await func(cls, request, *args, **kwargs)
            except InternalServerError as e:
                return web.json_response({
                    'status':StatusCodes.STATUS_INTERNAL_SERVER_ERROR.value,
                    'error':'internal server error'
                })
            except AlreadyExistsError as e:
                return web.json_response({
                    'status':StatusCodes.STATUS_CONFLIC.value,
                    'error':f'{e}'
                })
            except DoesNotExistsError as e:
                return web.json_response({
                    'status':StatusCodes.STATUS_NOT_FOUND.value,
                    'error':f'{e}'
                })    
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")               
                return web.json_response({
                    'status':StatusCodes.STATUS_INTERNAL_SERVER_ERROR.value,
                    'error':'db internal server error'
                })                     
            except Exception as e:
                logger.error(f'{func.__name__}:unknown exception:{e}')
                return web.json_response({
                    'status':StatusCodes.STATUS_INTERNAL_SERVER_ERROR.value,
                    'error':'super internal server error'
                })
        return inner
    return deco
def log_decorator():
    def deco(func):
        async def inner(cls, request: web.Request, *args, **kwargs):
            # Log details about the request
            data = await request.json()
            logger.debug(
                f'Request method: {request.method}, '
                f'Request path: {request.path}, '
                f'Request Body: {data}'
            )
            return await func(cls, request, *args, **kwargs)
        return inner
    return deco
def handle_auth():
    def deco(func):
        async def inner(cls,request: web.Request,*args,**kwargs):
            #print(func,"validate auth",args,kwargs)
            auth_header = request.headers.get("Authorization")
            if not auth_header: 
                return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.MISSING_AUTH_HEADER)
            bearer, access_token = auth_header.split(" ")
            if not bearer or bearer != "Bearer" : 
                return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.MISSING_BEARER_IN_TOKEN)
            if not access_token: 
                return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.MISSING_TOKEN_IN_HEADER)
            
            payload = request.app['permissions_service'].decode_user_token(access_token)
            exp = payload['exp']
            exp = datetime.datetime.fromtimestamp(exp)
            if exp < datetime.datetime.now(): 
                return create_response(StatusCodes.STATUS_UNAUTHORIZED,Errors.ACCESS_TOKEN_EXPIRE)
            user_id = payload['user_id'] 
            kwargs.update({"user_id":user_id})
            
            return await func(cls,request,*args,**kwargs)
        return inner
    return deco

def validate_online_user():
    def deco(func):
        async def inner(cls,request: web.Request,*args,**kwargs):
            user_id = kwargs['user_id']
            online_user = request.app['online_service'].get_online_user(user_id)
            kwargs.update({
                "nickname": online_user['nickname'],
                "user_color": online_user['color'],
            })
            return await func(cls,request,*args,**kwargs)
        return inner
    return deco

def validate_online_user_in_channel():
    def deco(func):
        async def inner(cls,request: web.Request,*args,**kwargs):
            user_id = kwargs['user_id']
            online_user = request.app['online_service'].get_online_user(user_id)
            online_channel = request.app['online_service'].get_channel_from_user_id(user_id)
            kwargs.update({
                "channel_name": online_channel['name'],
                "channel_color":online_channel['color']
            })
            kwargs.update({
                "nickname": online_user['nickname'],
                "user_color": online_user['color'],
            })
            return await func(cls,request,*args,**kwargs)
        return inner
    return deco



def validate_online_channel(channel_key):
    def deco(func):
        async def inner(cls,request: web.Request,*args,**kwargs):
            #print(func,"validate online channel",args,kwargs)
            channel_name = kwargs[channel_key]
            channel = request.app['messages_service'].get_channel(channel_name)
            channel_id = channel['id']
            online_channel = request.app['online_service'].get_online_channel(channel_id)
            online = online_channel['online']
            if online is not True:
                return create_response(StatusCodes.STATUS_FORBIDDEN, Errors.CHANNEL_IS_OFFLINE)
            kwargs.update({
                "channel_color": online_channel['color'],
                "channel_id": online_channel['id'],
            })
            return await func(cls,request,*args,**kwargs)
        return inner
    return deco


def validate_connected_online_channel():
    def deco(func):
        async def inner(request: web.Request,*args,**kwargs):
            #print(func,"validate connected online channel",args,kwargs)
            user_id = kwargs['user_id']
            channel_name = kwargs['channel_name']
            request.app['messages_service'].get_channel(channel_name)
            online_channel = request.app['online_service'].get_online_channel_by_name(channel_name)
            if online_channel['online'] == False: 
                return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.CHANNEL_IS_OFFLINE)
            channel_id = request.app['online_service'].get_user_online_channel_id(user_id)
            if not channel_id or not online_channel or online_channel['channel_id'] != channel_id: 
                return create_response(StatusCodes.STATUS_CONFLIC,Errors.USER_DOESNT_NOT_EXISTS_IN_CHANNEL)
            return await func(request,*args,**kwargs)
        return inner
    return deco

def handle_request_params(keys: typing.List[str]):
    def deco(func):
        async def inner(cls,request: web.Request,*args,**kwargs):
            data = await request.json()
            for key in keys:
                if not data.get(key):
                    return web.json_response({"status":StatusCodes.STATUS_BAD_REQUEST.value,'error': f"Must provide {key} in request {func.__name__}"})
            kwargs.update(data)
            
            return await func(cls,request,*args,**kwargs)
        return inner
    return deco

def is_black_list(block_type:BlockType=BlockType.NONE):
    def deco(func):
        async def inner(request: web.Request, *args, **kwargs):
            user_id = kwargs['user_id']            
            block = request.app["permissions_service"].get_user_block_status(user_id)
            if block_type.value is not None:
                if block_type.value is BlockType.BAN.value:
                    if block["ban"] is True:
                        return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.USER_IS_BANNED_ERROR_MSG)            
                if block_type.value is BlockType.READONLY.value:
                    if block["readonly"] is True or block['ban'] is True:
                        return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.USER_IS_READONLY_ERROR_MSG)            
            return await func(request, *args, **kwargs)
        return inner
    return deco

def has_user_access():
    def deco(func):
        async def inner(cls,request: web.Request, *args, **kwargs):
            #print(func,"has access",kwargs)
            channel_name = kwargs[""]
            user_id = kwargs["user_id"]
            channel = request.app['messages_service'].get_channel(channel_name)                
            channel_role = channel['role_id']            
            try:
                user = request.app["users_service"].get_user_by_id(user_id)
                role_id = user['role_id']
            except DoesNotExistsError as e:
                role_id = request.app['permissions_service'].get_role_by_role_type(RoleType.GUEST)['id']
                
            is_granted_channel_permissions =request.app['permissions_service'].has_permissions_by_role(role_id,channel_role)
            if is_granted_channel_permissions is False:
                return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.NO_PERMISSION_ERROR_MSG)       
            return await func(cls,request, *args, **kwargs)
        return inner
    return deco


def has_channel_access(channel_key):
    def deco(func):
        async def inner(cls,request: web.Request, *args, **kwargs):
            #print(func,"has access",kwargs)
            channel_name = kwargs[channel_key]
            user_id = kwargs["user_id"]
            channel = request.app['messages_service'].get_channel(channel_name) 
            channel_role = channel['role_id']            
            try:
                user = request.app["users_service"].get_user_by_id(user_id)
                role_id = user['role_id']
            except DoesNotExistsError as e:
                role_id = request.app['permissions_service'].get_role_by_role_type(RoleType.GUEST)['id']                
            is_granted_channel_permissions =request.app['permissions_service'].has_permissions_by_role(role_id,channel_role)  
            if is_granted_channel_permissions is False:
                return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.NO_PERMISSION_ERROR_MSG)       
            return await func(cls,request, *args, **kwargs)
        return inner
    return deco

def has_permissions(permission_name:str,block_type:BlockType=BlockType.NONE):
    def deco(func):
        async def inner(request: web.Request, *args, **kwargs):
            channel_name = kwargs['channel_name']
            user_id = kwargs["user_id"]
            channel = request.app['messages_service'].get_channel(channel_name)
            channel_role = channel['role_id']            
            user = request.app["users_service"].get_user_by_id(user_id)
            is_granted_channel_permissions =request.app['permissions_service'].has_permissions_by_role(user['role'],channel_role)
            is_granted_by_permission_name =request.app['permissions_service'].has_permissions_by_permission_name(permission_name)
            if is_granted_by_permission_name is False:
                return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.NO_PERMISSION_ERROR_MSG)
            block = request.app["permissions_service"].get_user_block_status(user_id)
            if block_type.value is not None:
                if block_type.value == BlockType.BAN.value:
                    if block["ban"] == True:
                        return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.USER_IS_BANNED_ERROR_MSG)            
                if block_type.value == BlockType.READONLY.value:
                    if block["readonly"] == True:
                        return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.USER_IS_READONLY_ERROR_MSG)            
            if is_granted_by_permission_name is False or is_granted_channel_permissions is False:
                return create_response(StatusCodes.STATUS_FORBIDDEN,Errors.NO_PERMISSION_ERROR_MSG)            
            
            return await func(request, *args, **kwargs)
            
        return inner
    return deco














































# def validate_auth():
#     def deco(func):
#         async def inner(request: web.Request,*args,**kwargs):
#             data = await request.json()
#             request.headers.get("")
#             token = data.get("user_token")
#             if not token:
#                 return create_response(StatusCodes.STATUS_BAD_REQUEST,Errors.MISSING_TOKEN_IN_HEADER)
#             user_id = request.app['permissions_service'].decode_user_token(token)
#             kwargs.update({
#                 "user_id": user_id,
#             })
#             # await request.pop("user_token")
#             # request.update({"user_id":user_id})

#             # auth_data = request.headers.get("Authorization")
#             # if not auth_data:
#             #     return web.json_response({"status":StatusCodes.STATUS_UNAUTHORIZED,"error":Errors.MISSING_AUTH_HEADER})
#             # bearer,token = auth_data.split(" ")
#             # if not bearer:
#             #     return web.json_response({"status":StatusCodes.STATUS_UNAUTHORIZED,"error":Errors.MISSING_BEARER_IN_TOKEN})
#             # if not token:
#             #     return web.json_response({"status":StatusCodes.STATUS_UNAUTHORIZED,"error":Errors.MISSING_TOKEN_IN_HEADER})
            
#             # payload = request.app['permissions_service'].decode_user_token(token)

#             #if payload['ext] old , return need to refresh token
#             #user_id, 
#             # check if user_id exists
#             # return not exists , invalid token,
#             return await func(request,*args,**kwargs)
#         return inner
#     return deco


















# def validate_permissions(keys: typing.List[str]):
#     def deco(func):
#         async def inner(request: web.Request,*args,**kwargs):
#             data = await request.json()
#             for key in keys:
#                 if not data.get(key):
#                     print({f"error Must provide {key}. in func {func.__name__}"})
#                     return web.json_response({"status":StatusCodes.STATUS_BAD_REQUEST.value,'error': f"Must provide {key} in request {func.__name__}"})
#             return await func(request,*args,**kwargs)
#         return inner
#     return deco



# def validate_online_channel():
#     def deco(func):
#         def inner(self, data, *args, **kwargs):
#             user_id = data.get("channel_name")
#             for online_user in self._online_users:
#               if online_user.id == user_id:
#                   return func(self, data, *args, **kwargs)
#             for online_channel,online_channel_users in self._online_channels.items():
#               online_channel_users_cp = online_channel_users.copy()
#               for online_channel_user in online_channel_users_cp:
#                   if online_channel_user.id == user_id:
#                       return func(self, data, *args, **kwargs)
#             return func(self, data, *args, **kwargs)
#         return inner
#     return deco






# def handle_response(on_error_print_channel=True,):
#     def deco(func):
#         async def inner(self,data,*args,**kwargs):
#             res = await func(data,*args,**kwargs)
#             if isinstance(res,str):
#                 if on_error_print_channel:
#                     self.channel_window.add_line(res)
#                     return
#             if isinstance(res,dict):
#                 pass
            
            
#         return inner
#     return deco

# def validate_func_params(keys: typing.List[str]):
#     def deco(func):
#         def inner(self, data: web.Request, *args, **kwargs):
#             for key in keys:
#                 if isinstance(data,str):
#                     print("who are u",data, func.__name__)
#                 if not data.get(key):
#                     print({f"error Must provide {key}. in func {func.__name__}"})
#                     return {"status":StatusCodes.STATUS_BAD_REQUEST.value,"error": f"Must provide {key}."}

#             return func(self, data, *args, **kwargs)
#         return inner
#     return deco

# # def validate_online_user_connected():
# #     def deco(func):
# #         def inner(self, data, *args, **kwargs):
# #             user_id = data.get("user_id")
# #             for online_user in self._online_users:
# #               if online_user.id == user_id:
# #                   return func(self, data, *args, **kwargs)
# #             for online_channel,online_channel_users in self._online_channels.items():
# #               online_channel_users_cp = online_channel_users.copy()
# #               for online_channel_user in online_channel_users_cp:
# #                   if online_channel_user.id == user_id:
# #                       return func(self, data, *args, **kwargs)
# #             return func(self, data, *args, **kwargs)
# #         return inner
# #     return deco




# def permiss():
#     def deco(func):
#         async def inner(request: web.Request,*args,**kwargs):
#             data = await request.json()
#             token = data.get("user_token")
#             is_granted = request.app["permissions_service"].has_permissions(token)
#             if is_granted is False:
#                 return web.json_response({'status':StatusCodes.STATUS_UNAUTHORIZED.value,'error': Errors.NOT_ALLOWED.value})
#             return await func(request,*args,**kwargs)
#         return inner
#     return deco


# def token_required():
#     def deco(func):
#         async def inner(request: web.Request,*args,**kwargs):
#             data = await request.json()
#             token = data.get("user_token")
#             if not token:
#                 return web.json_response({'status':StatusCodes.STATUS_BAD_REQUEST.value,'error': "must provide token for this operation"})
#             user_id = request.app["users_service"].decode_user_token(token)
#             del request['user_token']
#             request.update({"user_id":user_id})
#             return await func(request,*args,**kwargs)
#         return inner
#     return deco






