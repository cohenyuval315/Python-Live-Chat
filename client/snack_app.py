import asyncio
from command_handler import CommandHandler
from exceptions import ErrorMessage, ExitException,ExpiredException,ClientException,CredentialsException,ServerException
from view.channel_window import ChannelWindow
from managers.channel_manager import ChannelManager
from managers.users_manager import UsersManager
from managers.chat_manager import ChatManager
from managers.creds_manager import CredentialsManager
from apis.auth_api import AuthAPI
from apis.channel_api import ChannelAPI
from apis.chat_api import ChatAPI
from apis.user_api import UserAPI
from logger import logger

class SnackChatClient():
    UPDATE_ONLINE_CHANNELS_DELAY = 10
    UPDATE_ONLINE_USERS_DELAY = 5
    UPDATE_CHAT_MESSAGES_LOOP = 1

    def __init__(self):
        logger.info('create client instance')
        self.auth_api = AuthAPI()
        self.user_api = UserAPI()
        self.channel_api = ChannelAPI()
        self.chat_api = ChatAPI()    
        self.channel_window = ChannelWindow(add_input_lines_to_text=False)
        
        self.channel_manager = ChannelManager(self.channel_window,self.channel_api)
        self.users_manager = UsersManager(self.channel_window,self.user_api)
        self.chat_manager = ChatManager(self.channel_window,self.chat_api)
        self.creds_manager = CredentialsManager(self.channel_window,self.auth_api)
        self.command_handler = CommandHandler(
            self.channel_window,
            self.creds_manager,
            self.channel_manager,
            self.chat_manager,
            self.users_manager,
            )

    def set_channel_window(self, channel_window):
        self.channel_window = channel_window

    async def init(self,nickname=None,username=None,password=None):
        logger.info('starting...')
        try:
           
            await self.creds_manager.init_identity(nickname,username,password)
        except CredentialsException as e: 
            logger.error(f"creds exception: {e}", exc_info=True)
            return
        
        while True:
            try:
                await self.start()
            except ClientException as e:
                logger.info(f"client exception: {e}", exc_info=True)
            except ExpiredException as e:
                await self.creds_manager.refresh_access_token()
                continue
            except ServerException as e:
                logger.info('server error...')
            except ExitException as e:       
                logger.info('exit exception')
                break
            except Exception as e:
                logger.info('unknown exception')
                break
    

    async def start(self):
        
        tasks = [
            self.run_window(),
            self.update_chat_messages_loop(),
            self.update_connected_users(),
            self.post_messages_loop(),
            self.update_online_channels()
        ]
    
        await asyncio.gather(*tasks,return_exceptions=True)




    async def run_window(self):
        await self.channel_window.run()

    async def update_online_channels(self):
        while True:
            user_token = await self.creds_manager.get_token()
            await self.channel_manager.update(user_token)
            await asyncio.sleep(self.UPDATE_ONLINE_CHANNELS_DELAY)

    async def update_connected_users(self):
        while True:
            channel_name = await self.chat_manager.get_current_channel()
            token = await self.creds_manager.get_token()
            nickname = await self.creds_manager.get_nickname()
            await self.users_manager.update(channel_name,nickname,token)
            await asyncio.sleep(self.UPDATE_ONLINE_USERS_DELAY)
            
    async def update_chat_messages_loop(self):
        while True:   
            token = await self.creds_manager.get_token()            
            await self.chat_manager.update(token)     
            await asyncio.sleep(self.UPDATE_CHAT_MESSAGES_LOOP)

    async def post_messages_loop(self):
        while True:
            user_input = await self.channel_window.get_next_input_line()
            await self.command_handler.handle_input(user_input)

    async def close(self):
        await self.creds_manager.exit()
