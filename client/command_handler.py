from constants.client_commands import ClientCommands
from constants.client_globals import ClientGlobals
from utils import is_valid_status

class CommandHandler():
    INVALID_COMMAND = "invalid command"
    INVALID_ARGS = "invalid command args"
    COMMAND_START = "/"

    def __init__(self,
                 channel_window,
                 creds_manager,
                 channel_manager,
                 chat_manager,
                 users_manager) -> None:
        self.channel_window = channel_window
        self.creds_manager = creds_manager
        self.channel_manager = channel_manager
        self.chat_manager = chat_manager
        self.users_manager = users_manager


    async def help_glossary(self) -> str:
        help_string  = ""
        for key,val in ClientCommands.HELP_MSG.value.items():
            help_string += f"{key} : {val} \n"
        return help_string

    async def handle_output(self,res):
        if not res:
            return
        if isinstance(res,str):
            return self.channel_window.add_line(res,'gray')
        if not is_valid_status(res,True):
            self.channel_window.add_line(res['error'])

    async def handle_input(self,user_input:str):
        if user_input == "":
            return
        channel_name = await self.chat_manager.get_current_channel()
        token = await self.creds_manager.get_token()        
        if not user_input.startswith(self.COMMAND_START):
            if channel_name == ClientGlobals.LOBBY.value:
                return self.channel_window.add_line(user_input)
            return await self.chat_manager.get_api().post_message(user_input,token)
        command_input = user_input.split(' ')        
        res = await self.handle_command(command_input,channel_name,token)
        return await self.handle_output(res)

    async def handle_command(self,command_input:list[str],channel_name,token):
        if len(command_input) == 1:
            command = command_input[0]
            if command not in ClientCommands.NO_ARGS_COMMANDS.value:
                return self.INVALID_COMMAND
            if command == ClientCommands.COMMAND_PRINT_HELP.value:
                return await self.help_glossary()
            if command == ClientCommands.COMMAND_EXIT_CLIENT.value:
                return await self.creds_manager.exit() 
            if command == ClientCommands.COMMAND_EXIT_CHANNEL.value:
                return await self.chat_manager.exit_channel(token)
            if command == ClientCommands.COMMAND_CLEAR_CHAT_MSGS.value:
                return await self.chat_manager.clear_view()
            if command == ClientCommands.COMMAND_DELETE_CHANNEL.value:
                return await self.channel_manager.get_api().delete_channel(channel_name,token)
            if command == ClientCommands.COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE.value:
                return await self.channel_manager.get_api().promote_channel(channel_name,token)
            if command == ClientCommands.COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE.value:
                return await self.channel_manager.get_api().demote_channel(channel_name,token)
            if command == ClientCommands.COMMAND_CLEAR_CHANNEL_DATABASE.value:
                return await self.channel_manager.get_api().delete_channel_messages(channel_name,token)
            if command == ClientCommands.COMMAND_CLEAR_DATABASE.value:
                return await  self.channel_manager.get_api().delete_all_messages(token)
        if len(command_input) == 2:
            command = command_input[0]
            arg = command_input[1]
            if command not in ClientCommands.ONE_ARG_COMMANDS.value:
                return self.INVALID_COMMAND
            if command == ClientCommands.COMMAND_CREATE_CHANNEL.value:
                return await self.channel_manager.get_api().create_channel(arg,token)
            if command == ClientCommands.COMMAND_DELETE_CHANNEL.value:
                return await self.channel_manager.get_api().delete_channel(arg,token) 
            if command == ClientCommands.COMMAND_UPDATE_CHANNEL_NAME.value:
                return await self.channel_manager.get_api().update_channel_name(channel_name,arg,token)
            if command == ClientCommands.COMMAND_CHANGE_CHANNEL.value:
                return await self.chat_manager.change_channel(arg,token)
            if command == ClientCommands.COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE.value:
                return await self.channel_manager.get_api().promote_channel(channel_name,token)
            if command == ClientCommands.COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE.value:
                return await self.channel_manager.get_api().demote_channel(channel_name,token)
            if command == ClientCommands.COMMAND_BAN_USER.value:
                return await self.users_manager.get_api().ban_user(channel_name,arg,token)
            if command == ClientCommands.COMMAND_UNBAN_USER.value:
                return await self.users_manager.get_api().unban_user(channel_name,arg,token)
            if command == ClientCommands.COMMAND_READ_ONLY_USER.value:
                return await self.users_manager.get_api().silence_user(channel_name,arg,token)
            if command == ClientCommands.COMMAND_ALLOW_WRITE_USER.value:
                return await self.users_manager.get_api().unsilence_user(channel_name,arg,token)
            if command == ClientCommands.COMMAND_PROMOTE_USER.value:
                return await self.users_manager.get_api() .promote_user(arg,token)
            if command == ClientCommands.COMMAND_DEMOTE_USER.value:
                return await self.users_manager.get_api().demote_user(arg,token)
            if command == ClientCommands.COMMAND_CLEAR_CHANNEL_DATABASE.value:
                return await self.channel_manager.get_api().delete_channel_messages(arg,token)
        return self.INVALID_ARGS


    