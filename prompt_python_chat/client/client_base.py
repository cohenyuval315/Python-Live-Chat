from yarl import URL
from prompt_python_chat.constants import StatusCodes,Endpoints
from prompt_python_chat.exceptions import ExpiredException
import aiohttp
import typing
import jwt
import asyncio
from aiohttp import BasicAuth
class ClientBase:
    #headers=headers,ssl=True
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    default_headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    def __init__(self, base_url):
        self._base_url:URL  = base_url
    
    def _make_url(self,path: str):
        return self._base_url.join(URL(path))

    def set_channel_window(self, channel_window):
        self.channel_window = channel_window

    async def _method(self,session:aiohttp.ClientSession, method: str, path , json: dict) -> dict:
        if method.upper() == self.GET:
            return await self._get(session,path,json)
        if method.upper() == self.POST:
            return await self._post(session,path,json)
        if method.upper() == self.DELETE:
            return await self._delete(session,path,json)        
        if method.upper() == self.PUT:
            return await self._put(session,path,json)
        return {"error": "fail to create request"}
        
    async def _get(self,session:aiohttp.ClientSession, path, json:dict) -> dict:
        async with session.get(path,json=json) as resp:
            return await resp.json()

    async def _post(self,session:aiohttp.ClientSession, path, json:dict) -> dict:
        async with session.post(path,json=json) as resp:
            return await resp.json()

    async def _delete(self,session:aiohttp.ClientSession, path, json: dict) -> dict:
        async with session.delete(path,json=json) as resp:
            return await resp.json()

    async def _put(self,session:aiohttp.ClientSession, path, json: dict) -> dict:
        async with session.put(path,json=json) as resp:
            return await resp.json()

    async def _async_request(self,method: str,path:Endpoints, json: dict={},headers:dict={},SSL:bool=False, access_token=None,refresh_token=None) -> dict:
        auth_header = None
        if access_token:         
            auth_header = {
                "Authorization": f"Bearer {access_token}"
            }
            self.default_headers.update(auth_header)
        url = self._make_url(path.value)
        res = {}
        async with aiohttp.ClientSession(headers=self.default_headers) as session:
            session.headers['Authorization'] = f"Bearer {access_token}"
            res = await self._method(session,method,url,json)
            if res['status'] == 401:
                raise ExpiredException("")
        return res

            #print(res)
        #     if res['status'] == 401:
        #         new_access_t
            
        #     if not res.get('status'):
        #         pass
        #     if res['status'] not in StatusCodes.SUCCESS_STATUS_CODES.value:
        #         return res['error']
            
        #     if res.get('data'):
        #         return res['data']
        #     print(res)
        # return {}
    