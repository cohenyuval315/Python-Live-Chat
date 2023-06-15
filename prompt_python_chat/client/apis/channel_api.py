from client_base import ClientBase
from prompt_python_chat.constants import Endpoints,RoleType
from client_errors import ClientErrors
import asyncio

class ChannelAPI(ClientBase):
    async def get_all_channels(self,token) -> dict:
        res =  await self._async_request(method=self.GET,path=Endpoints.GET_ALL_CHANNELS,json={},access_token=token)
        return res        
    
    async def update_channel_name(self,channel_name:str,new_name:str,token) -> dict:
        json = {
            "update_channel_name":channel_name,
            "new_name":new_name
        }        
        res = await self._async_request(self.PUT,Endpoints.PUT_UPDATE_CHANNEL_NAME,json,access_token=token)
        return res

    async def promote_channel(self,channel_name:str,token) -> dict:
        json = {
            "promote_channel_name":channel_name,
        }        
        res = await self._async_request(self.PUT,Endpoints.PUT_UPDATE_PROMOTE_CHANNEL,json,access_token=token)
        return res

    async def demote_channel(self,channel_name:str,token)-> dict:
        json = {
            "demote_channel_name":channel_name,
        }         
        res = await self._async_request(self.PUT,Endpoints.PUT_UPDATE_DEMOTE_CHANNEL,json,access_token=token)
        return res

    async def create_channel(self,channel_name:str,token) -> dict:
        json = {
            "create_channel_name":channel_name,
        }        
        res = await self._async_request(self.POST,Endpoints.POST_CREATE_CHANNEL,json,access_token=token)
        return res

    async def delete_channel(self,channel_name:str,token) -> dict:
        json = {
            "delete_channel_name":channel_name,
        }        
        res = await self._async_request(self.DELETE,Endpoints.DELETE_DELETE_CHANNEL,json,access_token=token)
        return res

    async def delete_channel_messages(self,channel_name:str,token) -> dict:
        json = {
            "channel_name":channel_name,
        }        
        res = await self._async_request(self.DELETE,Endpoints.DELETE_CHANNEL_MESSAGES,json=json,access_token=token)
        return res    


    async def delete_all_messages(self,token) -> dict:
        res = await self._async_request(self.DELETE,Endpoints.DELETE_ALL_MESSAGE,{},access_token=token)
        return res            
    