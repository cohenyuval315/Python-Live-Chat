from aiohttp import web
from prompt_python_chat.exts import metadata_obj
from prompt_python_chat.constants import StatusCodes,ColorType,RoleType,BlockType
from prompt_python_chat.decorators import handle_request_params,handle_auth,has_permissions,has_user_access

class UserController():

    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_UPDATE_USER_ROLE)
    @handle_request_params(['target_nickname'])
    async def promote_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        role = request.app["permissions_service"].get_role_by_role_type(RoleType.MOD)
        role = role['data']
        role_id = role['id']
        result = request.app['users_service'].update_user_role(user_nickname,role_id)
        return web.json_response(result)



    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_UPDATE_USER_ROLE)
    @handle_request_params(['target_nickname'])
    async def demote_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        role = request.app["permissions_service"].get_role_by_role_type(RoleType.USER)
        role = role['data']
        role_id = role['id']  
        result = request.app['userss_service'].update_user_role(data)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_POST_BLOCK)    
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def unblock_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_id = kwargs['user_id']
        channel_id = kwargs['channel_id']
        result = request.app['snack_server_service'].unblock_user(user_id,channel_id)
        return web.json_response(result)
    




    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_GET_USERS)
    async def get_all_users(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        result = request.app["users_service"].get_users()
        return web.json_response(result)




    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_UPDATE_USER_ROLE)
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def ban_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_id = kwargs['channel_id']
        user_id = kwargs['user_id']
        result = request.app['permissions_service'].block_user(channel_id,user_id,BlockType.BAN)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_POST_BLOCK)
    @has_user_access()
    @handle_request_params(['target_nickname'])
    async def silence_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_id = kwargs['channel_id']
        user_id = kwargs['user_id']
        result = request.app['permissions_service'].block_user(channel_id,user_id,BlockType.READONLY)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_DELETE_USER)
    @handle_request_params(["target_nickname"])
    async def delete_user(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_nickname = data.get("target_nickname")
        result = request.app['users_service'].delete_user(user_nickname)
        return web.json_response(result)
