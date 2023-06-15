from client_base import ClientBase
from prompt_python_chat.constants import Endpoints

class ChatAPI(ClientBase):
    async def post_message(self, content:str,token) -> dict:
        json = {
                'content': content,
                }
        res = await self._async_request(self.POST,Endpoints.POST_MESSAGE,json=json,access_token=token)
        return res
        
    async def get_channel_messages(self,channel_last_msg_index:int,token) -> dict:
        json = {"current_msg_index":str(channel_last_msg_index),
                }
        res =  await self._async_request(self.GET,Endpoints.GET_CHANNEL_MESSAGES,json=json,access_token=token)
        return res
    
    async def change_channel(self,new_channel_name: str, token) -> dict:
        json = {"new_channel_name":new_channel_name}
        res =  await self._async_request(self.POST,Endpoints.CHANGE_CHANNEL,json=json,access_token=token)
        return res
    
    async def exit_channel(self,token) -> dict:
        res = await self._async_request(self.POST,Endpoints.EXIT_CHANNEL,access_token=token)
        return res