import enum

class ClientCommands(enum.Enum):
    
    COMMAND_PRINT_HELP = "/help"
    COMMAND_EXIT_CLIENT = "/exit"

    COMMAND_CHANGE_CHANNEL = "/channel"    
    COMMAND_CREATE_CHANNEL = "/create"
    COMMAND_DELETE_CHANNEL = "/delete"
    COMMAND_EXIT_CHANNEL = "/lobby"

    COMMAND_UPDATE_CHANNEL_NAME = "/ch-name"
    COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE = "/ch-promote"
    COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE = "/ch-demote"

    COMMAND_BAN_USER = "/ban"
    COMMAND_UNBAN_USER = "/unban"

    COMMAND_READ_ONLY_USER = "/silence"
    COMMAND_ALLOW_WRITE_USER = "/unsilence"

    COMMAND_PROMOTE_USER = "/promote"
    COMMAND_DEMOTE_USER = "/demote"

    COMMAND_CLEAR_CHAT_MSGS = "/clear"

    COMMAND_CLEAR_CHANNEL_DATABASE = "/dbclear"
    COMMAND_CLEAR_DATABASE = "/dbclear-all"
        

    NO_ARGS_COMMANDS = [
        COMMAND_PRINT_HELP,
        COMMAND_EXIT_CLIENT,
        COMMAND_EXIT_CHANNEL,
        COMMAND_CLEAR_CHAT_MSGS,
        COMMAND_DELETE_CHANNEL,
        COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE,
        COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE,
        COMMAND_CLEAR_CHANNEL_DATABASE,
        COMMAND_CLEAR_DATABASE
    ]
    
    ONE_ARG_COMMANDS = [
        COMMAND_CHANGE_CHANNEL,
        COMMAND_CREATE_CHANNEL,
        COMMAND_DELETE_CHANNEL,
        COMMAND_UPDATE_CHANNEL_NAME,
        COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE,
        COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE   ,
        COMMAND_BAN_USER,
        COMMAND_UNBAN_USER,
        COMMAND_READ_ONLY_USER,
        COMMAND_ALLOW_WRITE_USER,
        COMMAND_PROMOTE_USER,
        COMMAND_DEMOTE_USER,
        COMMAND_CLEAR_CHANNEL_DATABASE
    ]

    HELP_MSG = {
        "\n----- HELP -----" : "",
        "command [ARGS]:" : "description",        
        "page up to scroll upward":"",
        "page down to scroll downward":"",
        COMMAND_PRINT_HELP : "help",
        COMMAND_EXIT_CLIENT : "exit",
        COMMAND_EXIT_CHANNEL : "leave channel",
        COMMAND_CLEAR_CHAT_MSGS : "clear the chat",
        COMMAND_CLEAR_DATABASE:"clear all channels chats for everyone",
        f"{COMMAND_DELETE_CHANNEL} (none | channel-name)" : "(delete this channel | delete a channel)",
        f"{COMMAND_UPDATE_CHANNEL_NAME} (none | channel-name) ":"(change this channel name | change a channel name)" ,
        f"{COMMAND_UPDATE_CHANNEL_PERMISSIONS_PROMOTE} (none | channel-name) ":"(promote this channel | promote a channel) to higher permissions",
        f"{COMMAND_UPDATE_CHANNEL_PERMISSIONS_DEMOTE} (none | channel-name)  ":"(demote this channel | demote a channel) to lower permissions",
        f"{COMMAND_CLEAR_CHANNEL_DATABASE} (none | channel-name) ":"(clear this channel | clear a channel) chat for everyone",
        f"{COMMAND_CHANGE_CHANNEL}":"",
        f"{COMMAND_CREATE_CHANNEL}":"",
        f"{COMMAND_BAN_USER}":"",
        f"{COMMAND_UNBAN_USER}":"",
        f"{COMMAND_READ_ONLY_USER}":"",
        f"{COMMAND_ALLOW_WRITE_USER}":"",
        f"{COMMAND_PROMOTE_USER}":"",
        f"{COMMAND_DEMOTE_USER}":"",     
    }
