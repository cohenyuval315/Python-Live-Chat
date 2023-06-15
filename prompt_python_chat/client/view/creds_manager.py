from .channel_window import ChannelWindow
from prompt_python_chat.client.apis.auth_api import AuthAPI
from .manager_base import ManagerBase
from prompt_python_chat.utils import is_valid_status
from prompt_python_chat.exceptions import ExitException,CredentialsException,ClientException

class CredentialsManager(ManagerBase):
    def __init__(self, channel_window: ChannelWindow,auth_api:AuthAPI) -> None:
        super().__init__(channel_window)
        self.channel_window = channel_window
        self.auth_api = auth_api
        self.access_token = None
        self.refresh_token = None
        self.nickname = None

    def get_api(self) -> AuthAPI:
        return self.auth_api
    
    async def get_token(self):
        return self.access_token
    
    async def set_token(self,token):
        self.access_token = token

    async def get_nickname(self):
        return self.nickname
    
    async def print_view(self):
        if self.nickname:
            self.channel_window.change_identity(self.nickname)
        else:
            self.channel_window.change_identity("error")

    async def refresh_access_token(self):
        res = await self.auth_api.refresh_token(self.refresh_token,self.access_token)
        if not is_valid_status(res):
            pass
        res = res['data']
        self.access_token = res['access_token']

    async def init_identity(self,nickname=None,username=None,password=None):
        res = await self.handle_creds(nickname,username,password)
        if not is_valid_status(res):
            raise CredentialsException(res)
        res = res['data']
        self.access_token = res['access_token']
        self.refresh_token = res['refresh_token']
        self.nickname = res['nickname']
        return await self.print_view()
        
    async def handle_creds(self,nickname=None,username=None,password=None) -> dict:
        if not username and not password:
            res = await self.auth_api.login_guest()
            return res
        if nickname and username and password:
            res = await self.auth_api.sign_up(nickname,username,password)
            if res['status'] != 201:
                return res
        if username and password:
            res =  await self.auth_api.login_user(username,password)
            return res
        return {}

    async def exit(self):
        self.channel_window.exit()
        await self.auth_api.logout(self.access_token)
