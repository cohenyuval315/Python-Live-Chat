from aiohttp import web
from decorators import handle_request_params,handle_auth,log_decorator,exception_handler

from constants import StatusCodes,ColorType,RoleType


class AuthController():
    @classmethod
    @exception_handler()
    @log_decorator()
    async def ping(cls,request:web.Request,*args,**kwargs):
        return web.json_response({"status":StatusCodes.STATUS_OK.value})

    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_request_params(["username","password"])
    async def login_user(cls,request:web.Request,*args,**kwargs):
        
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        user_res = request.app["users_service"].login_user(username,password)
        user = user_res
        role_res = request.app['permissions_service'].get_role_by_id(user['role_id'])
        role = role_res
        role_color = role['color']
        online_user_res = request.app['online_service'].user_login(user['id'],user['nickname'],ColorType(role_color))
        online_user = online_user_res

        access_token = request.app['permissions_service'].generate_user_access_token(online_user['id'])
        refresh_token = request.app['permissions_service'].generate_user_refresh_token(online_user['id'])
        res = {
            "status":StatusCodes.STATUS_OK.value,
            "data":{
                "access_token":access_token,
                "refresh_token":refresh_token,
                "nickname":online_user['nickname'],
                "color":role_color                
            }
        }
        return web.json_response(res)

    @classmethod
    @exception_handler()
    @log_decorator()
    async def login_guest(cls,request:web.Request,*args,**kwargs):
        data = await request.json()
        guest_user_res = request.app["users_service"].login_guest()
        user = guest_user_res
        role_res = request.app['permissions_service'].get_role_by_role_type(RoleType.GUEST)
        role = role_res
        role_color = role['color']
        online_user_res = request.app['online_service'].user_login(user['id'],user['nickname'],ColorType(role_color))
        online_user = online_user_res

        access_token = request.app['permissions_service'].generate_user_access_token(online_user['id'])
        refresh_token = request.app['permissions_service'].generate_user_refresh_token(online_user['id'])
        res = {
            "status":StatusCodes.STATUS_OK.value,
            "data":{
                "access_token":access_token,
                "refresh_token":refresh_token,
                "nickname":online_user['nickname'],
                "color":role_color
            }
        }
        return web.json_response(res)

    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_request_params(["nickname","username","password"])
    async def sign_up(cls,request:web.Request,*args,**kwargs):
        data = await request.json()
        username = data.get("username")
        nickname = data.get("nickname")
        password = data.get("password")
        role_res = request.app['permissions_service'].get_role_by_role_type(RoleType.USER)
        role = role_res
        role_id = role['id']
        new_user_res = request.app["users_service"].create_user(nickname,username,password,role_id)
        
        return web.json_response({"status":StatusCodes.STATUS_CREATED.value})

    
    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    async def refresh_access_token(cls,request:web.Request,*args,**kwargs):
        data = await request.json()
        refresh = data.get("refresh_token")
        access = data.get("access_token")

        refresh_payload = request.app['permissions_service'].decode_token(refresh)
        access_payload = request.app['permissions_service'].decode_token(access)
        if access_payload['user_id'] != refresh_payload['user_id']:
            return web.json_response(status=StatusCodes.STATUS_UNAUTHORIZED.value,text="invalid tokens validation")
        new_access_token = request.app['permissions_service'].refresh_access_token(access)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":new_access_token
        }
        return web.json_response(res)


    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    async def logout_user(cls,request:web.Request,*args,**kwargs):
        user_id = kwargs['user_id']
        request.app["online_service"].user_logout(user_id)
        res = {
            "status":StatusCodes.STATUS_OK.value
        }
        return web.json_response(res)
