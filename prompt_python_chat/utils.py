import base64
import bcrypt
import base64
import jwt
from prompt_python_chat.constants import StatusCodes,Errors
from typing import Union,List 
from datetime import datetime, timedelta
from prompt_python_chat.exceptions import ServerException,ExpiredException,ClientException,ExitException
ACCESS_TOKEN_LIFETIME_MINUTES = 30
REFRESH_TOKEN_LIFETIME_DAYS =  30

def generate_access_token(user_id:int,secret_key):
    expires_in = timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES)
    exp = datetime.utcnow() + expires_in
    payload = {
        'user_id': user_id,
        'exp': exp
    }
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return access_token

def generate_refresh_token(user_id:int,secret_key):
    expires_in = timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS)
    exp = datetime.utcnow() + expires_in
    payload = {
        'user_id': user_id,
        'exp': exp
    }
    refresh_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return refresh_token


def create_response(status:StatusCodes,error_msg:Errors=Errors.UNKNOWN_ERROR,data: Union[dict,List] = {}):
    status = status.value # type: ignore
    error_status_codes = StatusCodes.ERROR_STATUS_CODES.value
    if status in error_status_codes:
        res =  {
            "status": status,
            "error": error_msg.value
        }            
        return res
    success_status_codes = StatusCodes.SUCCESS_STATUS_CODES.value
    if status in success_status_codes:
        res = {
            "status":status,
            "data":data
        }
        return res
    raise Exception("shouldnt get here bad create response")


def is_valid_status(res:dict,raise_exceptions=False):
    status = res['status'] 
    if raise_exceptions:
        if len(res) == 0: 
            raise ClientException("empty result")    
        if status == StatusCodes.STATUS_INTERNAL_SERVER_ERROR.value:
            raise ServerException(res['error'])
        if status == StatusCodes.STATUS_UNAUTHORIZED.value:
            raise ExpiredException(res['error'])
        if status == StatusCodes.STATUS_BAD_REQUEST.value:
            raise ClientException(res['error'])
    if status in [code for code in StatusCodes.SUCCESS_STATUS_CODES.value]:
        return True
    return False


def generate_token(user_id,secret_key):
    payload = {'user_id': user_id}
    # TOKEN_TIME = 10
    # payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=TOKEN_TIME)

    # payload['session_id']
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# def refresh_token(token,secret_key):
#     generate_token()

def decode_token(token,secret_key):
    try:
        payload = jwt.decode(token,secret_key, algorithms=['HS256'])
        return payload
    except jwt.exceptions.InvalidTokenError:
        return None


def generate_password_hash(password, salt_rounds=12):
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt(salt_rounds))
    encoded = base64.b64encode(hashed)
    return encoded.decode('utf-8')


def check_password_hash(encoded, password):
    password = password.encode('utf-8')
    encoded = encoded.encode('utf-8')

    hashed = base64.b64decode(encoded)
    is_correct = bcrypt.hashpw(password, hashed) == hashed
    return is_correct


def create_connection_string(config, memory=False):
    if memory:
        return config.SQLITE_MEMORY_URI
    else:
        return f"{config.DB_SYSTEM}+{config.DB_SYSTEM_CONNECTOR}://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        
