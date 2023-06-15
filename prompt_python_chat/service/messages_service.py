from .base_service import BaseService
from prompt_python_chat.constants import StatusCodes,ColorType,Errors
from prompt_python_chat.db_dao import channel_dao,chat_dao
from datetime import datetime
from prompt_python_chat.utils import create_response
class MessagesService(BaseService):

    def create_channel(self,channel_name:str,role_id:int):
        if channel_dao.get_channel_by_name(channel_name):
            return create_response(StatusCodes.STATUS_CONFLIC,Errors.CHANNEL_EXISTS_ERROR_MSG)      
        res = channel_dao.create_channel(channel_name=channel_name,role_id=role_id)
        if res:
            return create_response(StatusCodes.STATUS_CREATED,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.CREATE_CHANNEL_ERROR_MSG)
        
    def delete_channel(self,channel_name:str):
        channel = channel_dao.get_channel_object_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
        res = channel_dao.delete_channel(channel)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_CHANNEL_ERROR_MSG)
        
    def update_channel_name(self,channel_name:str,new_name:str):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)

        channel = channel_dao.get_channel_by_name(new_name)
        if not channel:
            return create_response(StatusCodes.STATUS_CONFLIC,Errors.CHANNEL_EXISTS_ERROR_MSG)                
        
        res = channel_dao.update_channel_name(channel['id'],new_name)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)        
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UPDATE_CHANNEL_ERROR_MSG)
        
    def update_channel_role(self,channel_name:str,new_role_id:int):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
        res = channel_dao.update_channel_role(channel['id'],role_id=new_role_id)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UPDATE_CHANNEL_ERROR_MSG)    

    def delete_channel_messages(self,channel_name:str):
        channel =  channel_dao.get_channel_object_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
        res = chat_dao.delete_channel_messages(channel.id)
        if not res:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_CHANNEL_MSG_ERROR_MSG)
        res = channel_dao.delete_channel(channel)
        if not res:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_CHANNEL_ERROR_MSG)
        return create_response(StatusCodes.STATUS_OK,data=res)

    def get_all_channels(self):
        channels = channel_dao.get_all_channels()
        if channels:
            res = [{"name":channel['name'] ,"color":channel['color']} for channel in channels] 
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.GET_ALL_CHANNELS_ERROR_MSG)    
        
    def _get_all_channels(self):
        channels = channel_dao.get_all_channels()
        if channels:
            return create_response(StatusCodes.STATUS_OK,data=channels)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.GET_ALL_CHANNELS_ERROR_MSG)    

    def _normalize_msg(self,msg):
        datetime_object = datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        time = datetime_object.strftime("%Y-%m-%d %H:%M")
        normalized_msg = {
            "message":f"{time} {msg['nickname']}: {msg['content']}",
            "color":msg['color']
        }
        return normalized_msg
        
    def get_channel_messages(self, channel_name:str,user_current_channel_msg_index:int):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
        channel_id = channel['id']
        channel_msgs = chat_dao.get_channel_messages(channel_id)
        last_index = -1
        num_msgs = len(channel_msgs)
        if num_msgs > 0:
            last_index = channel_msgs[num_msgs - 1]['index']
            channel_msgs = channel_msgs[int(user_current_channel_msg_index) + 1:]
        normalized_msgs = []
        for msg in channel_msgs:
            normalized_msgs.append(self._normalize_msg(msg))
        res = {
            "last_index":last_index,
            "messages":normalized_msgs,
            "channel_name":channel_name
        }
        return create_response(StatusCodes.STATUS_OK,data=res)
    
    def post_message(self, user_id:int,nickname:str,channel_name:str,content:str,color:ColorType):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
        res = chat_dao.post_message(channel['id'],user_id,nickname,content,color)
        if not res:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.CREATE_MSG_ERROR)
        return create_response(StatusCodes.STATUS_OK,data=res)    

    def delete_all_messages(self):
        res = chat_dao.delete_all_message()
        if not res:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_ALL_MESSAGES_ERROR_MSG) 
        return create_response(StatusCodes.STATUS_OK,data=res)
    
    def get_channel(self,channel_name:str):
        channel =  channel_dao.get_channel_by_name(channel_name)
        if channel:
            return create_response(StatusCodes.STATUS_OK,data=channel)
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.CHANNEL_DOES_NOT_EXISTS_ERROR_MSG)
    
