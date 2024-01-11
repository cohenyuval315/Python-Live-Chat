from .client_base import ClientBase
from constants import Endpoints

class AuthAPI(ClientBase):

    async def refresh_token(self,refresh_token,access_token) -> dict:
        res = await self._async_request(method=self.GET,path=Endpoints.GET_REFRESH_TOKEN,refresh_token=refresh_token, access_token=access_token)
        return res

    async def sign_up(self,nickname:str,username:str,password:str) -> dict:
        json = {"nickname":nickname,
                "username":username,
                "password":password}
        res = await self._async_request(method=self.POST,path=Endpoints.POST_SIGNUP,json=json)
        return res 

    async def login_user(self,username:str,password:str) -> dict :
        json = {
            'username': username,
            "password":password,
        }
        res = await self._async_request(method=self.POST,path=Endpoints.POST_LOGIN,json=json)
        return res
    
    async def login_guest(self) -> dict:
        res = await self._async_request(method=self.POST,path=Endpoints.POST_LOGIN_GUEST,json={})
        return res

    async def logout(self,token) -> dict:
        res = await self._async_request(method=self.POST,path=Endpoints.POST_LOGOUT,json={},access_token=token)
        return res