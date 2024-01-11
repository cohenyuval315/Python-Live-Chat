from .base_service import BaseService
from constants import ColorType
from db_dao import channel_dao,chat_dao
from datetime import datetime
import utils as u
from exceptions import InternalServerError,AlreadyExistsError,DoesNotExistsError
from typing import Optional

def _normalize_msg(msg):
    datetime_object = datetime.strptime(msg['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    time = datetime_object.strftime("%Y-%m-%d %H:%M")
    normalized_msg = {
        "message":f"{time} {msg['nickname']}: {msg['content']}",
        "color":msg['color']
    }
    return normalized_msg
class MessagesService(BaseService):

    def create_channel(self,channel_name:str,role_id:int):
        if channel_dao.get_channel_by_name(channel_name):
            raise AlreadyExistsError('channel already exists')  
        res = channel_dao.create_channel(channel_name=channel_name,role_id=role_id)
        if res:
            return res
        raise InternalServerError('create_channel internal error')
        
    def delete_channel(self,channel_name:str):
        channel = channel_dao.get_channel_object_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel doest not exists')  
        res = channel_dao.delete_channel(channel)
        if res:
            return res
        raise InternalServerError('delete_channel internal error')
        
    def update_channel_name(self,channel_name:str,new_name:str):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel doest not exists')  
        channel = channel_dao.get_channel_by_name(new_name)
        if not channel:
            raise AlreadyExistsError('channel already exists')
        
        res = channel_dao.update_channel_name(channel['id'],new_name)
        if res:
            return res     
        raise InternalServerError('update_channel_name internal error')
        
    def update_channel_role(self,channel_name:str,new_role_id:int):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel does not exists')  
        res = channel_dao.update_channel_role(channel['id'],role_id=new_role_id)
        if res:
            return res
        raise InternalServerError('update_channel_role internal error')

    def delete_channel_messages(self,channel_name:str):
        channel =  channel_dao.get_channel_object_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel does not exists')
        res = chat_dao.delete_channel_messages(channel.id)
        if res:
            res = channel_dao.delete_channel(channel)
            if res:
                return res     
            else:
                raise InternalServerError('delete_channel_messages internal error')
        else:
            raise InternalServerError('delete_channel_messages internal error')

    def get_all_channels(self):
        channels = channel_dao.get_all_channels()
        if channels:
            res = [{"name":channel['name'] ,"color":channel['color']} for channel in channels] 
            return res
        raise InternalServerError('get_all_channels internal error')
        
    def _get_all_channels(self):
        channels = channel_dao.get_all_channels()
        if channels:
            return channels
        return []
        raise InternalServerError('_get_all_channels internal error')

        


        
    def get_channel_messages(self, channel_name:str,user_current_channel_msg_index:int):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel does not exists')
        channel_id = channel['id']
        channel_msgs = chat_dao.get_channel_messages(channel_id)
        last_index = -1
        num_msgs = len(channel_msgs)
        if num_msgs > 0:
            last_index = channel_msgs[num_msgs - 1]['index']
            channel_msgs = channel_msgs[int(user_current_channel_msg_index) + 1:]
        normalized_msgs = []
        for msg in channel_msgs:
            normalized_msgs.append(_normalize_msg(msg))
        res = {
            "last_index":last_index,
            "messages":normalized_msgs,
            "channel_name":channel_name
        }
        return res
    
    def post_message(self, user_id:Optional[int],nickname:str,channel_name:str,content:str,color:ColorType):
        channel = channel_dao.get_channel_by_name(channel_name)
        if not channel:
            raise DoesNotExistsError('channel does not exists')
        res = chat_dao.post_message(channel['id'],user_id,nickname,content,color)
        if res:
            return res
        
        raise InternalServerError('post_message internal error')

    def delete_all_messages(self):
        res = chat_dao.delete_all_message()
        if res:
            return res
        raise InternalServerError('delete_all_messages internal error')
    
    def get_channel(self,channel_name:str):
        channel =  channel_dao.get_channel_by_name(channel_name)
        if channel:
            return channel
        raise DoesNotExistsError('channel does not exists')
    
