import enum

class RequestParams(enum.Enum):
    CHANNEL_NAME = "channel_name"
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class Constants(enum.Enum):
    NONE = None
    GUEST_NICKNAME = "anon"
    LOBBY = "lobby"
    LOBBY_MSG = "please use /help for more information \npage up = scroll up \npage down = scroll down"

class ColorType(enum.Enum):
    NONE = None
    RED = "red"
    BLUE = "blue"
    PINK = "pink"
    GREEN = "green"
    YELLOW = "yellow"
    WHITE = "white"

class BlockType(enum.Enum):
    NONE = None
    READONLY = "READONLY"
    BAN = "BAN"

class RoleType(enum.Enum):
    NONE = None
    GUEST = "GUEST"
    USER = "USER"
    MOD = "MOD"
    ADMIN = "ADMIN"      


class Endpoints(enum.Enum):
    PING ='/ping'
    GET_TOKEN = "/token"
    GET_REFRESH_TOKEN = "/refresh"
    DELETE_ALL_MESSAGE = "/allmessages"
    EXIT_CHANNEL = "/channel/exit"
    DELETE_CHANNEL_MESSAGES = "/channel/allmessages"
    GET_ALL_USERS = "/users"
    PUT_USER_ROLE = "/user/role"
    PUT_PROMOTE_USER = "/user/promote"
    PUT_DEMOTE_USER = "/user/demote"
    DELETE_USER = "/users"
    POST_LOGIN = "/login"
    POST_LOGIN_GUEST = "/login/guest"
    POST_SIGNUP = "/sign_up"
    POST_LOGOUT = "/logout"
    GET_CHANNEL_MESSAGES = "/messages"
    POST_MESSAGE = "/message"
    GET_CHANNEL_ONLINE_USERS = "/channel/users"
    GET_ALL_CHANNELS = "/channels"
    POST_BAN_USER = "/user/ban"
    POST_READ_ONLY_USER = "/user/readonly"
    DELETE_UNBLOCK_USER = "/user/block"
    POST_CREATE_CHANNEL = "/channels"
    DELETE_DELETE_CHANNEL = "/channels"
    PUT_UPDATE_CHANNEL_NAME = "/channel/name"
    PUT_UPDATE_CHANNEL_ROLE = "/channel/role"
    CHANGE_CHANNEL ="/change"
    PUT_UPDATE_PROMOTE_CHANNEL = "/channel/promote"
    PUT_UPDATE_DEMOTE_CHANNEL = "/channel/demote"

class StatusCodes(enum.Enum):
    STATUS_OK = 200
    STATUS_CREATED = 201

    STATUS_NOT_MODIFIED = 304
    STATUS_BAD_REQUEST = 400
    STATUS_UNAUTHORIZED = 401
    STATUS_NOT_FOUND = 404
    STATUS_METHOD_NOT_ALLOWED = 405
    STATUS_FORBIDDEN = 403
    STATUS_CONFLIC = 409
    STATUS_TOO_MANY_REQUESTS = 429
    STATUS_INTERNAL_SERVER_ERROR = 500

    SUCCESS_STATUS_CODES = [
        STATUS_CREATED,
        STATUS_OK
    ]    
    ERROR_STATUS_CODES = [
        STATUS_NOT_MODIFIED,
        STATUS_BAD_REQUEST,
        STATUS_UNAUTHORIZED,
        STATUS_NOT_FOUND,
        STATUS_CONFLIC,
        STATUS_METHOD_NOT_ALLOWED,
        STATUS_FORBIDDEN,
        STATUS_TOO_MANY_REQUESTS,
        STATUS_INTERNAL_SERVER_ERROR
    ] 

class Errors(enum.Enum):
    ACCESS_TOKEN_EXPIRE = "access token expired"
    UNKNOWN_ERROR = "unknown error"

    CREATE_USER_ERROR_MSG = "fail to user creation"
    DELETE_USER_ERROR_MSG = "fail to delete user"
    UPDATE_USER_ERROR_MSG = "fail to update user"
    GET_ALL_USERS_ERROR_MSG = "fail to get all users"
    USERNAME_DOES_NOT_EXISTS = "username does not exists"
    USER_DOES_NOT_EXISTS_ERROR_MSG = "user does not exists" 
    WRONG_PASSWORD_ERROR_MSG = "wrong password"
    USERNAME_EXISTS_ERROR_MSG = "username already exists"
    NICKNAME_EXISTS_ERROR_MSG = "nickname already exists"
    UNAUTH = "unauth for this operation"
    NO_ROLE_ERROR_MSG = "role doesnt exists"

    NO_PERMISSION_ERROR_MSG = "no permission for this operation"
    BLOCK_EXISTS_ERROR_MSG = "block type already exists for this user in this channel"
    DELETE_BLOCK_ERROR_MSG = "fail to delete block"
    CHANNEL_IS_OFFLINE = "channel is offline"
    ROLE_NAME_ERROR_MSG = "invalid role"
    

    CHANNEL_EXISTS_ERROR_MSG="channel already exists"
    GET_ALL_CHANNELS_ERROR_MSG = "fail to get all channels"
    
    CHANNEL_DOES_NOT_EXISTS_ERROR_MSG = "channel does not exists"
    BLOCK_DOES_NOT_EXISTS_ERROR_MSG = "block is not exists"
    CREATE_CHANNEL_ERROR_MSG = "fail to create channel"
    CREATE_BLOCK_ERROR_MSG = "fail to create block"
    UPDATE_CHANNEL_ERROR_MSG = "fail to update channel"
    CREATE_MSG_ERROR = "fail to create message in this channel"
    DELETE_CHANNEL_ERROR_MSG = "fail to delete channel"
    DELETE_CHANNEL_MSG_ERROR_MSG = "fail to delete msg in delete channel"

    USER_IS_BANNED_ERROR_MSG = "user is banned from this channel"
    USER_IS_READONLY_ERROR_MSG = "user is read only in this channel"
    INVALID_BLOCK_TYPE_ERROR_MSG = "invalid block type"
    DELETE_ALL_MESSAGES_ERROR_MSG = "fail to delete all messages"


    ONLINE_USER_DOES_NOT_EXISTS = "online user does not exists"
    ONLINE_CHANNEL_DOES_NOT_EXISTS = "online channel does not exists"
    UNABLE_TO_UNCONNECT_USER_FROM_CHANNEL = "fail to log out user from channel"
    UNABLE_TO_UNCONNECT_USER = "fail to log out user to offline"
    MISSING_AUTH_HEADER = "auth header is missing"
    MISSING_BEARER_IN_TOKEN = "bearer in header is missing"
    MISSING_TOKEN_IN_HEADER = "token is missing"

    UNABLE_TO_CONNECT_USER_TO_CHANNEL = "fail to connect user to channel"
    USER_DOESNT_NOT_EXISTS_IN_CHANNEL = "user is not connected to any channel"

    
# class JsonSchemas():
#     response_schema = {
#         "type": "object",
#         "properties": {
#             "status": {
#                 "type": "int",
#                 "minLength" : 3,
#                 "maxLength" : 100
#             },
#             "error": {
#                 "type": "string"
#             },
#             "data": {
#                 "type": "object"
#             }            
#         },
#         "required" : ["status"],
#         "oneOf": [{"required": ["error"]}, {"required": ["data"]}]
#     }

    
#     CREATE_CHANNEL_JSON = {
#         "channel_name": "" # some string value , either create or check 

#     }

