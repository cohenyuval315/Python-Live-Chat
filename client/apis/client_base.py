from yarl import URL
from constants import Endpoints
from exceptions import ExpiredException,ErrorMessage
import aiohttp

import os
SERVER_HOST = os.environ.get('SERVER_HOST','127.0.0.1')
SERVER_PORT = os.environ.get('SERVER_PORT','8082')
BASE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

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

    def __init__(self):
        self._base_url = BASE_URL

    def _make_url(self,path: str):
        return f"{self._base_url}{path}"

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
            if res['status'] > 300:
                
                raise ErrorMessage(res['error'])
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
    