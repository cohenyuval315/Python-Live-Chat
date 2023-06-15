from .dataclasses import OnlineChannel,OnlineUser
from typing import Optional,List
from .base_service import BaseService
from prompt_python_chat.constants import StatusCodes,Errors, ColorType
from prompt_python_chat.utils import create_response

class OnlineService(BaseService):
    _online_users:set[OnlineUser] = set()
    _online_channels:set[OnlineChannel]= set()     
  
    def user_change_channel(self,user_id:int,channel_id:int):
        online_user = self.get_online_user_object(user_id)
        if not online_user:
             return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_USER_DOES_NOT_EXISTS)
        online_channel = self._get_online_channel(channel_id)
        if not online_channel:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_CHANNEL_DOES_NOT_EXISTS)
        self._unconnect_user_from_online_channel_by_id(user_id,channel_id)
        if self._is_user_connected_to_channel(user_id):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UNABLE_TO_UNCONNECT_USER_FROM_CHANNEL)
        self._connect_user_to_online_channel(online_user,channel_id)
        if not self._is_user_connected_to_channel(user_id):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UNABLE_TO_CONNECT_USER_TO_CHANNEL)
        online_channel = self.get_channel_from_user_id(user_id)
        if not online_channel.get('data'):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR)
        online_channel = online_channel['data']
        res = {
            "channel_name": online_channel['name'],
            "channel_id":online_channel['id']
        }
        return create_response(StatusCodes.STATUS_OK,data=res)
    
    def user_exit_channel(self,user_id:int):
        online_user = self.get_online_user_object(user_id)
        if not online_user:
             return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_USER_DOES_NOT_EXISTS)
        if not self._is_user_connected_to_channel(user_id):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.USER_DOESNT_NOT_EXISTS_IN_CHANNEL)
        self._unconnect_user_from_online_channels(user_id)
        if self._is_user_connected_to_channel(user_id):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UNABLE_TO_UNCONNECT_USER_FROM_CHANNEL)
        return create_response(StatusCodes.STATUS_OK)
    
    def get_channel_from_user_id(self,user_id:int):
        for channel in OnlineService._online_channels.copy():
            users = channel.users.copy()
            for user in users:
                if user.user_id == user_id:
                    return create_response(StatusCodes.STATUS_OK,data=self._return_online_channel(channel))
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_CHANNEL_DOES_NOT_EXISTS)
        
    def user_logout(self, user_id:int):
        self._unconnect_user_from_online_channels(user_id)
        if self._is_user_connected_to_channel(user_id):
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UNABLE_TO_UNCONNECT_USER_FROM_CHANNEL)
        self._unconnect_user_from_online(user_id)
        online_user  = self._get_online_user(user_id)
        if online_user:
           return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UNABLE_TO_UNCONNECT_USER) 
        return create_response(StatusCodes.STATUS_OK)
    
    def user_login(self,user_id:int,nickname:str,color:ColorType):
        self._connect_user_online(user_id,nickname,color)
        online_user = self._get_online_user(user_id)
        if not online_user:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.ONLINE_USER_DOES_NOT_EXISTS)
        return create_response(StatusCodes.STATUS_OK,data=online_user)

    def get_online_channel_by_name(self,channel_name:int) -> Optional[dict]:
        for channel in OnlineService._online_channels.copy():
            if channel.name == channel_name:
                return create_response(StatusCodes.STATUS_OK,data=self._return_online_channel(channel))
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_CHANNEL_DOES_NOT_EXISTS)
            
    def get_online_channel(self,channel_id:int) -> Optional[dict]:
        for channel in OnlineService._online_channels.copy():
            if channel.channel_id == channel_id:
                return create_response(StatusCodes.STATUS_OK,data=self._return_online_channel(channel))
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_CHANNEL_DOES_NOT_EXISTS)            

    def get_online_user(self,user_id:int) -> Optional[dict]:
        for user in OnlineService._online_users.copy():
            if user.user_id == user_id:
                return create_response(StatusCodes.STATUS_OK,data=self._return_online_user(user))
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.ONLINE_USER_DOES_NOT_EXISTS)

    def get_channel_online_users(self,channel_id:int):
        online_users = []
        for channel in self._online_channels.copy():
            if channel.channel_id == channel_id:
                users = channel.users.copy()
                for user in users:
                    online_users.append(self._return_online_user(user))
        return create_response(StatusCodes.STATUS_OK,data=online_users)











    def _get_online_channel(self,channel_id:int) -> Optional[dict]:
        for channel in OnlineService._online_channels.copy():
            if channel.channel_id == channel_id:
                return self._return_online_channel(channel)
            
    def _get_online_user(self,user_id:int) -> Optional[dict]:
        for user in OnlineService._online_users.copy():
            if user.user_id == user_id:
                return self._return_online_user(user)

    def get_online_user_object(self,user_id:int) -> Optional[OnlineUser]:
        for user in OnlineService._online_users.copy():
            if user.user_id == user_id:
                return user



    
    def _set_channels(self, channels:List[dict]):
        OnlineService._online_channels = set(OnlineChannel(channel_id=channel['id'],name=channel['name'],color=channel['color'],online=True,users=set()) for channel in channels)


    def _return_online_channel(self,channel:OnlineChannel) -> dict:
        return {
            "id":channel.channel_id,
            "name":channel.name,
            "color":channel.color,
            "online":channel.online,
            "users": [self._return_online_user(user) for user in channel.users.copy()]
        }

    def _return_online_user(self,user:OnlineUser) -> dict:
        return {
            "id":user.user_id,
            "nickname":user.nickname,
            "color":user.color
        }

    def _return_online_users(self,online_users:List[OnlineUser]) -> List[dict]:
        return [self._return_online_user(user) for user in online_users]

    def _return_online_channels(self,online_channels:List[OnlineChannel]) -> List[dict]:
        return [self._return_online_channel(channel) for channel in online_channels]


    def _remove_channel(self,channel_id:int):
        online_channels = OnlineService._online_channels.copy() 
        for channel in online_channels:
            if channel.channel_id == channel_id:
                OnlineService._online_channels.remove(channel)

    def _add_channel(self,channel_id:int,channel_name:str,color:ColorType):
        channel = OnlineChannel(online=True,channel_id=channel_id,name=channel_name,users=set(),color=color.value)
        OnlineService._online_channels.add(channel)

    def _update_channel_name(self,channel_id:int,new_name:str):
        online_channels = OnlineService._online_channels.copy()
        for channel in online_channels:
            if channel.channel_id == channel_id:
                channel.set_name(new_name)
        OnlineService._online_channels = online_channels

    def _update_channel_online_status(self,channel_id:int,status=True):
            online_channels = OnlineService._online_channels.copy()
            for channel in online_channels:
                if channel.channel_id == channel_id:
                    channel.set_online(status)
            self._online_channels = online_channels

    def _is_user_connected_to_channel(self,user_id) -> bool:
        for channel in OnlineService._online_channels.copy():
            users = channel.users.copy()
            for user in users:
                if user.user_id == user_id:
                    return True
        return False

    def get_user_online_channel_id(self,user_id:int):
        online_channels = OnlineService._online_channels.copy()
        for channel in online_channels:
            for user in channel.users.copy():
                if user.user_id == user_id:
                    return channel.channel_id

    def _connect_user_online(self,user_id:int,nickname:str,color:ColorType):
        user = OnlineUser(user_id=user_id,nickname=nickname,color=color.value)
        OnlineService._online_users.add(user)

    def _connect_user_to_online_channel(self,user:OnlineUser,channel_id:int):
        online_channels = OnlineService._online_channels.copy()
        for channel in online_channels:
            if channel.channel_id == channel_id:
                channel.add_user(user)
        self._online_channels = online_channels
        
    def _is_channel_online(self,channel_id:str):
        online_channels = OnlineService._online_channels.copy()
        for channel in online_channels:
            if channel.channel_id == channel_id:
                return channel.online
    
    def _is_user_online(self,user_id:int) -> bool:
        for user in OnlineService._online_users.copy():
            if user.user_id == user_id:
                return True
        return False

    def _unconnect_user_from_online(self,user_id:int):  
        for user in self._online_users.copy():
            if user.user_id == user_id:
                OnlineService._online_users.remove(user)
     
    def _unconnect_user_from_online_channels(self,user_id:int):
        online_channels = OnlineService._online_channels.copy()
        for channel in online_channels:
            channel.remove_user_by_id(user_id)
        OnlineService._online_channels = online_channels

    def _unconnect_all_users_from_online_channel(self,channel_id:str):
        online_channels = OnlineService._online_channels.copy()             
        for channel in online_channels:
            if channel.channel_id == channel_id:
                channel.users = set()
        OnlineService._online_channels = online_channels
    
    def _unconnect_user_from_online_channel_by_nickname(self,nickname:str, channel_id:int):
        online_channels = OnlineService._online_channels.copy()             
        for channel in online_channels:
            if channel.channel_id == channel_id:
                channel.remove_user_by_nickname(nickname)
        OnlineService._online_channels = online_channels

    def _unconnect_user_from_online_channel_by_id(self,user_id:int, channel_id:int):
        online_channels = OnlineService._online_channels.copy()             
        for channel in online_channels:
            if channel.channel_id == channel_id:
                channel.remove_user_by_id(user_id)
        OnlineService._online_channels = online_channels
        