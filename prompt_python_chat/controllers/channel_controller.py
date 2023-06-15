from aiohttp import web
from prompt_python_chat.decorators import handle_request_params,validate_online_user,handle_auth,has_permissions,has_channel_access,validate_online_channel
from prompt_python_chat.exts import metadata_obj
from prompt_python_chat.constants import StatusCodes,ColorType
from prompt_python_chat.utils import is_valid_status
class ChannelController():
    
    @classmethod
    @handle_auth()
    @handle_request_params(["content"])
    @validate_online_user()
    @validate_online_channel("channel_name")
    @has_channel_access('channel_name')
    async def post_message(cls,request:web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        content = data.get("content")
        user_id = kwargs['user_id']
        nickname = kwargs['nickname']
        user_color = ColorType(kwargs['user_color'])
        channel_name = kwargs['channel_name']
        #channel_color = ColorType(kwargs['channel_color'])
        result = request.app["messages_service"].post_message(user_id,nickname,channel_name,content,user_color)
        return web.json_response(result)

    @classmethod
    @handle_auth()
    @handle_request_params(["current_msg_index"])
    async def get_channel_messages(cls,request:web.Request,*args,**kwargs):
        data = await request.json()
        current_msg_index = data.get("current_msg_index")
        user_id = kwargs['user_id']
        res = request.app["online_service"].get_channel_from_user_id(user_id)
        if not is_valid_status(res):
            return res
        res = res['data']
        channel_name = res['name']
        print("user index",current_msg_index)
        result = request.app["messages_service"].get_channel_messages(channel_name,current_msg_index)
        print(result)
        return web.json_response(result)

    @classmethod
    @handle_auth()
    @handle_request_params(["new_channel_name"])
    @validate_online_user()
    @validate_online_channel("new_channel_name")
    @has_channel_access('new_channel_name')
    async def change_channel(cls,request:web.Request,*args,**kwargs) -> web.Response:
        new_channel_name = kwargs['new_channel_name']
        channel = request.app['online_service'].get_online_channel_by_name(new_channel_name)
        channel = channel['data']
        user_id = kwargs['user_id']
        result = request.app['online_service'].user_change_channel(user_id,channel['id'])
        return web.json_response(result)
    

    @classmethod
    @handle_auth()
    async def exit_channel(cls,request:web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_id = kwargs['user_id']
        result = request.app['online_service'].user_logout(user_id)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    async def get_channel_online_users(cls,request:web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        user_id = kwargs['user_id']
        channel = request.app["online_service"].get_channel_from_user_id(user_id)
        channel = channel['data']
        res = request.app["online_service"].get_channel_online_users(channel['id'])
        if res.get('data'):
            users = res['data']
            channel_users = []
            for user in users:
                channel_users.append({
                    "nickname":user['nickname'],
                    "color":user['color']
                })
            res = {
                "status":StatusCodes.STATUS_OK.value,
                "data":{
                    "users": channel_users
                }
            }
            return web.json_response(res)
        return web.json_response(status=StatusCodes.STATUS_INTERNAL_SERVER_ERROR.value)

    @classmethod
    @handle_auth()
    async def get_all_channels(cls,request:web.Request,*args,**kwargs) -> web.Response:  
        result = request.app['messages_service'].get_all_channels()
        return web.json_response(result)
        


    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_POST_CHANNEL)
    @handle_request_params(["create_channel_name"])
    async def create_channel(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        role_id = kwargs['role_id']
        result = request.app['messages_service'].create_channel(channel_name,role_id)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_channel_access("delete_channel_name")
    @has_permissions(metadata_obj.DB_DELETE_CHANNEL)
    @handle_request_params(["delete_channel_name"])
    async def delete_channel(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        result = request.app['messages_service'].delete_channel(channel_name)
        return web.json_response(result)

    @classmethod
    @handle_auth()
    @has_channel_access("update_channel_name")    
    @has_permissions(metadata_obj.DB_UPDATE_CHANNEL_NAME)
    @handle_request_params(["update_channel_name","new_name"])
    async def update_channel_name(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        new_name = data.get("new_name")
        result = request.app['messages_service'].update_channel_name(channel_name,new_name)
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_channel_access("promote_channel_name")    
    @has_permissions(metadata_obj.DB_UPDATE_CHANNEL_ROLE)
    @handle_request_params(["promote_channel_name"])
    async def promote_channel(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        new_role_id = kwargs['new_role_id']
        result = request.app['messages_service'].update_channel_role(channel_name,new_role_id)
        return web.json_response(result)

    @classmethod
    @handle_auth()
    @has_channel_access("demote_channel_name")        
    @has_permissions(metadata_obj.DB_UPDATE_CHANNEL_ROLE)
    @handle_request_params(["demote_channel_name"])
    async def demote_channel(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        new_role_id = kwargs['new_role_id']        
        result = request.app['messages_service'].update_channel_role(channel_name,new_role_id)
        return web.json_response(result)

    @classmethod
    @handle_auth()
    @has_permissions(metadata_obj.DB_CLEAR)    
    #@handle_request_params(["user_token"])
    async def delete_all_messages(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        result = request.app['messages_service'].delete_all_messages()
        return web.json_response(result)


    @classmethod
    @handle_auth()
    @has_channel_access('channel_name')
    @has_permissions(metadata_obj.DB_DELETE_CHANNEL_MSGS)
    @handle_request_params(['channel_name'])
    async def delete_channel_msgs(cls,request: web.Request,*args,**kwargs) -> web.Response:
        data = await request.json()
        channel_name = kwargs['channel_name']
        result = request.app['messages_service'].delete_channel_messages(channel_name)
        return web.json_response(result)
