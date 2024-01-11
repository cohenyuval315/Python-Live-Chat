from constants import StatusCodes
from exceptions import ServerException,ExpiredException,ClientException
ACCESS_TOKEN_LIFETIME_MINUTES = 30
REFRESH_TOKEN_LIFETIME_DAYS =  30



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
