from view.channel_window import ChannelWindow
from apis.user_api import UserAPI
from .manager_base import ManagerBase
from constants import ClientGlobals
from utils import is_valid_status

class UsersManager(ManagerBase):
    def __init__(self, channel_window: ChannelWindow,user_api:UserAPI) -> None:
        super().__init__(channel_window)
        self.channel_window = channel_window
        self.user_api = user_api
        self.channel_users = []

    def get_api(self) -> UserAPI:
        return self.user_api
    
    async def set_channel_users(self, users: list = []):
        for user in users:
            self.channel_users.append(user)
    
    async def print_view(self,clear=True):
        if clear:
            await self.clear_view()
        for channel_user in self.channel_users:
            self.channel_window.add_user(channel_user['nickname'],channel_user['color'])
        
    async def clear_view(self):
        self.channel_window.clear_users()
    
    async def clear_online_channel_users(self):
        self.channel_users.clear()

    @ManagerBase.catch_error_message
    async def update(self,channel_name,nickname,token):
        await self.clear_online_channel_users()
        if channel_name == ClientGlobals.LOBBY.value:
            await self.set_channel_users([{"nickname":nickname,"color":"white"}])
            await self.print_view()
        else:
            res = await self.user_api.get_online_users_in_channel(channel_name,token)
            if not is_valid_status(res):
                return self.channel_window.add_line(res['error'])
            res = res['data']
            users = res['users']            
            await self.set_channel_users(users)     
            await self.print_view()