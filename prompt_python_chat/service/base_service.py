from prompt_python_chat.constants import StatusCodes,Errors
from typing import Union,List
# try:
# # try something

# except SQLAlchemyError as e:
#   error = str(e.__dict__['orig'])
#   return error

class BaseService:
    def __init__(self) -> None:
        pass

    def create_response(self,status:StatusCodes,error_msg:Errors=Errors.UNKNOWN_ERROR,data: Union[dict,List] = {}):
        status = status.value
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



