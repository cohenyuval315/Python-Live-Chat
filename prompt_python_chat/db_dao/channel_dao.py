from typing import Optional,List
from prompt_python_chat.db_models import Channel,ChatMessage
from .base_dao import BaseDao
from sqlalchemy import update,delete,column,select

class ChannelDao(BaseDao):

    def _return_channel(self,channel:Channel):
        return {
            "id":channel.id,
            "name":channel.name,
            "role_id":channel.role_id,
            "color":channel.color.value,
        }
    
    def get_all_channels_objects(self) -> List[Channel]:
        return list(self.get_session().scalars(select(Channel)).all())
        
    def get_all_channels(self) -> List[dict]:
        _channels =  self.get_all_channels_objects()
        return [self._return_channel(channel) for channel in _channels]

    def get_channel_object_by_id(self, channel_id:int) -> Optional[Channel]:
        return self.get_session().scalars(select(Channel).where(Channel.id == channel_id)).one_or_none()
    
    def get_channel_by_id(self,channel_id:int) -> Optional[dict]:
        _channel = self.get_channel_object_by_id(channel_id)
        if _channel:
            return self._return_channel(_channel)

    def get_channel_object_by_name(self,channel_name:str) -> Optional[Channel]:
        return self.get_session().scalars(select(Channel).where(Channel.name == channel_name)).one_or_none()

    def get_channel_by_name(self,channel_name:str) -> Optional[dict]:
        _channel = self.get_channel_object_by_name(channel_name)
        if _channel:
            return self._return_channel(_channel)
    
    def is_channel_exists_by_id(self,channel_id:int) -> bool:
        if self.get_channel_object_by_id(channel_id):
            return True
        return False

    def is_channel_exists_by_name(self,channel_name:str) -> bool:
        if self.get_channel_object_by_name(channel_name):
            return True
        return False

    def update_channel_object_name(self,channel:Channel, new_name:str) -> Optional[Channel]:
        if channel.name != new_name:
            channel.name = new_name
            channel_id = channel.id 
            self.get_session().commit()
            updated_channel = self.get_channel_object_by_id(channel_id)
            if updated_channel and updated_channel.name == new_name:
                return updated_channel
        return channel

    def update_channel_name(self,channel_id:int, new_name:str) -> Optional[dict]:
        channel = self.get_channel_object_by_id(channel_id)
        if channel:
            updated_channel = self.update_channel_object_name(channel,new_name)
            if updated_channel:
                return self._return_channel(updated_channel)

    def update_channel_object_role(self,channel:Channel,role_id:int) -> Optional[Channel]:
        if channel.role_id != role_id:
            channel.role_id = role_id
            channel_id = channel.id 
            self.get_session().commit()
            updated_channel = self.get_channel_object_by_id(channel_id)
            if updated_channel and updated_channel.role_id == role_id:
                return updated_channel
        return channel

    def update_channel_role(self,channel_id:int,role_id) -> Optional[dict]:
        channel = self.get_channel_object_by_id(channel_id)
        if channel:
            updated_channel = self.update_channel_object_role(channel,role_id)     
            if updated_channel:
                return self._return_channel(updated_channel)

    def create_channel_object(self,channel_name:str, role_id:int) -> Optional[Channel]:
        channel_id = self.generate_id()
        new_channel = Channel(id=channel_id,name=channel_name,role_id=role_id)
        self.get_session().add(new_channel)
        self.get_session().commit()
        channel = self.get_channel_object_by_id(channel_id)        
        if channel:
            return channel

    def create_channel(self,channel_name:str, role_id:int) -> Optional[dict]:
        new_channel = self.create_channel_object(channel_name,role_id)
        if new_channel:
            return self._return_channel(new_channel)

    def get_delete_channel_object(self,channel:Channel) -> Optional[Channel]:
        delete_channel_id = channel.id
        self.get_session().delete(channel)
        self.get_session().commit()
        deleted_channel = self.get_channel_object_by_id(delete_channel_id)
        if not deleted_channel:
            return channel
        
    def delete_channel(self,channel:Channel) -> Optional[dict]:     
        deleted_channel = self.get_delete_channel_object(channel)
        if deleted_channel:
            return {"channel_id": deleted_channel.id}
        
    def delete_all_channel_msgs_by_id(self,channel_id:int) -> bool:
        msgs = self.get_session().scalars(select(ChatMessage).where(ChatMessage.channel_id == channel_id)).all()
        msgs_ids = []
        for msg in msgs:
            msgs_ids.append({"message_id": msg.id})
            self.get_session().delete(msg)
        self.get_session().commit()
        for msg_id in msgs_ids:
            if self.get_session().query(ChatMessage).filter_by(id=msg_id).first():
                return False
        return True
    
channel_dao = ChannelDao()