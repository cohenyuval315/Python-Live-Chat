from aiohttp import web
from exts import seed_data
from constants import RoleType,BlockType
from decorators import handle_request_params,exception_handler,log_decorator,handle_auth,has_permissions,has_user_access
from constants import StatusCodes
class UserController():

    @classmethod
    @exception_handler()
    @log_decorator()    
    @handle_auth()
    @has_permissions(seed_data.DB_UPDATE_USER_ROLE)
    @handle_request_params(['target_nickname'])
    async def promote_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        role = request.app["permissions_service"].get_role_by_role_type(RoleType.MOD)
        role = role
        role_id = role['id']
        result = request.app['users_service'].update_user_role(user_nickname,role_id)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)



    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_UPDATE_USER_ROLE)
    @handle_request_params(['target_nickname'])
    async def demote_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        role = request.app["permissions_service"].get_role_by_role_type(RoleType.USER)
        role = role
        role_id = role['id']  
        result = request.app['userss_service'].update_user_role(data)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)


    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_POST_BLOCK)    
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def unblock_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_id = kwargs['user_id']
        channel_id = kwargs['channel_id']
        result = request.app['snack_server_service'].unblock_user(user_id,channel_id)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)
    




    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_GET_USERS)
    async def get_all_users(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        result = request.app["users_service"].get_users()
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)



    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_UPDATE_USER_ROLE)
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def ban_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_id = kwargs['channel_id']
        user_id = kwargs['user_id']
        result = request.app['permissions_service'].block_user(channel_id,user_id,BlockType.BAN)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)


    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_POST_BLOCK)
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def silence_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_id = kwargs['channel_id']
        user_id = kwargs['user_id']
        result = request.app['permissions_service'].block_user(channel_id,user_id,BlockType.READONLY)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)


    @classmethod
    @exception_handler()
    @log_decorator()
    @handle_auth()
    @has_permissions(seed_data.DB_DELETE_USER)
    @handle_request_params(["target_nickname"])
    async def delete_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        result = request.app['users_service'].delete_user(user_nickname)
        res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":result
        }
        return web.json_response(res)
