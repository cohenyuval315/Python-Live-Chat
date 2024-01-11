import enum

class ClientGlobals(enum.Enum):
    ANONYMOUS = "anon"
    LOBBY='Lobby'
    NONE = None
    GUEST_NICKNAME = "anon"
    LOBBY_MSG = "please use /help for more information \npage up = scroll up \npage down = scroll down"
    CHANNEL_NAME = "channel_name"
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
