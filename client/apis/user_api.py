from .client_base import ClientBase
from constants import  Endpoints

class UserAPI(ClientBase):

    async def ban_user(self,channel_name:str,target_nickname:str,token) -> dict:
        json = {
            "target_nickname":target_nickname,
            "channel_name":channel_name,
        }
        res = await self._async_request(self.POST,Endpoints.POST_BAN_USER,json=json,access_token=token)
        return res

    async def silence_user(self,channel_name:str,target_nickname:str,token) -> dict:
            json = {
                "target_nickname":target_nickname,
                "channel_name":channel_name,
            }
            res = await self._async_request(self.POST,Endpoints.POST_READ_ONLY_USER,json,access_token=token)
            return res

    async def unban_user(self,channel_name:str,target_nickname:str,token) -> dict:
        json = {
            "target_nickname":target_nickname,
            "channel_name":channel_name,
        }        
        res = await self._async_request(self.DELETE,Endpoints.DELETE_UNBLOCK_USER,json=json,access_token=token)
        return res
    
    async def unsilence_user(self,channel_name:str,target_nickname:str,token) -> dict:
        return await self.unban_user(channel_name,target_nickname,token)
    
    async def promote_user(self,target_nickname:str,token) -> dict:
        json = {
            "target_nickname": target_nickname
        }        
        res = await self._async_request(self.PUT,Endpoints.PUT_PROMOTE_USER,json=json,access_token=token)
        return res
    
    async def demote_user(self,target_nickname:str,token) -> dict:
        json = {
            "target_nickname": target_nickname
        }        
        res = await self._async_request(self.PUT,Endpoints.PUT_DEMOTE_USER,json=json,access_token=token)
        return res

    async def get_online_users_in_channel(self,channel_name:str,token) -> dict:     
        res = await self._async_request(self.GET,Endpoints.GET_CHANNEL_ONLINE_USERS,json={
            channel_name:channel_name
        },access_token=token)
        return res

    async def get_all_users(self) -> dict:
        return {}
    
    async def delete_user(self) -> dict:
        return {}
