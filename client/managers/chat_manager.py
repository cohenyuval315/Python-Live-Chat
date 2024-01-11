from view.channel_window import ChannelWindow
from constants import ClientGlobals
from .manager_base import ManagerBase
from apis.chat_api import ChatAPI
from utils import is_valid_status
from exceptions import ErrorMessage



class ChatManager(ManagerBase):
    def __init__(self, channel_window: ChannelWindow,chat_api:ChatAPI) -> None:
        super().__init__(channel_window)
        self.channel_window = channel_window
        self.chat_api = chat_api
        self.current_channel_name = ClientGlobals.LOBBY.value
        self.current_channel_last_msg_index = -1        
        self.channel_messages_page = []
        self.init_lobby()

    def init_lobby(self):
        self.channel_window.clear_messages()
        self.channel_window.clear_users()        
        self.channel_window.change_header(f"{5 * '#'} {self.current_channel_name} {5 * '#'}")
        self.channel_window.add_line(ClientGlobals.LOBBY_MSG.value)


    def get_api(self) -> ChatAPI:
        return self.chat_api

    async def get_current_channel(self) -> str:
        return self.current_channel_name
    
    @ManagerBase.catch_error_message
    async def change_channel(self,channel_name: str,token):
        res = await self.chat_api.change_channel(channel_name,token)
        if channel_name == ClientGlobals.LOBBY.value:
            return self.init_lobby()
        if not is_valid_status(res):
            self.channel_window.add_line('invalid channel','gray')
            return res
        res = res['data']        
        updated_channel_name = res['channel_name']
        self.channel_window.clear_messages()
        self.channel_window.clear_users()
        self.current_channel_name = updated_channel_name
        self.current_channel_last_msg_index = -1
        self.channel_window.change_header(f"{5 * '#'} {self.current_channel_name} {5 * '#'}")

    @ManagerBase.catch_error_message
    async def exit_channel(self,token):
        try:
            if self.current_channel_name == ClientGlobals.LOBBY.value:
                return await self.print_view(True)     
            res = await self.chat_api.exit_channel(token)
            self.current_channel_name = ClientGlobals.LOBBY.value
            self.current_channel_last_msg_index = -1
            await self.print_view(True)
        except ErrorMessage as e:
            self.channel_window.add_line(f'{e}','gray')            

    async def set_messages_page(self,channel_messages:list = [],clear=True):
        if clear:
            await self.clear_messages_page()
        for message in channel_messages:
            self.channel_messages_page.append(message)

    
    async def print_view(self,clear=True):
        if clear:
            await self.clear_view()
        for message in self.channel_messages_page:
            self.channel_window.add_line(message['message'],message['color'])
    
    async def print_error(self,error_msg:str,debug=False):
        if debug:
            pass
        self.channel_window.add_line(error_msg)

    async def clear_view(self):
        self.channel_window.clear_messages()
        if self.current_channel_name == ClientGlobals.LOBBY.value:
            self.channel_window.add_line(ClientGlobals.LOBBY_MSG.value)
    
    async def clear_messages_page(self):
        self.channel_messages_page.clear()

    @ManagerBase.catch_error_message
    async def update(self,token):
        if self.current_channel_name == ClientGlobals.LOBBY.value:
            return
        else:
            res = await self.chat_api.get_channel_messages(self.current_channel_last_msg_index,token)
            if not is_valid_status(res):
                return self.channel_window.add_line(res['error'])
            res = res['data']
            channel_name = res['channel_name']
            last_index = res['last_index']
            messages = res['messages']
            self.current_channel_last_msg_index = int(last_index)
            self.current_channel_name = channel_name
            # if self.current_channel_last_msg_index == -1 and len(messages) == 0:
            #     await self.clear_view()
            #     return
            await self.set_messages_page(messages)
            await self.print_view(clear=False)
            
        
        
        

        