from .base_service import BaseService
from typing import Optional
import bcrypt
from prompt_python_chat.db_dao import user_dao
from prompt_python_chat.constants import StatusCodes,Errors
from uuid import uuid4 as v4
from prompt_python_chat.utils import create_response

class UsersService(BaseService):
    ANONYMOUS = "anon"

    def get_user_by_id(self,user_id:int):
        res =  user_dao.get_user_by_id(user_id)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.USER_DOES_NOT_EXISTS_ERROR_MSG)

    def login_user(self,username: str,password: str) -> Optional[dict]:
        if not user_dao.is_username_exists(username):
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.USERNAME_DOES_NOT_EXISTS)
        user = user_dao.get_user_by_username(username)
        if not user:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.USER_DOES_NOT_EXISTS_ERROR_MSG)
        if self._check_password(password,user['password']):
            return create_response(StatusCodes.STATUS_OK,data=user)
        return create_response(StatusCodes.STATUS_UNAUTHORIZED,Errors.WRONG_PASSWORD_ERROR_MSG)
        
    def login_guest(self):
        guest_id = int(str(v4().int)[:10])
        nickname = self.ANONYMOUS + "_" + str(guest_id)
        guest_data = {
            "id":guest_id,
            "nickname":nickname
        }
        return create_response(StatusCodes.STATUS_OK,data=guest_data)
       


    def create_user(self,nickname:str,username:str,password:str,role_id:int):
        if user_dao.is_username_exists(username):
            return create_response(StatusCodes.STATUS_CONFLIC,Errors.USERNAME_EXISTS_ERROR_MSG)
        if user_dao.is_nickname_exists(nickname):
            return create_response(StatusCodes.STATUS_CONFLIC,Errors.NICKNAME_EXISTS_ERROR_MSG)              
        res = user_dao.create_user(nickname,username,self._encrypt_password(password),role_id=role_id)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.CREATE_USER_ERROR_MSG)              
   
    def update_user_role(self,user_nickname:str,role_id:int):
        user = user_dao.get_user_by_nickname(user_nickname)
        if not user:
            return create_response(StatusCodes.STATUS_NOT_FOUND, Errors.USER_DOES_NOT_EXISTS_ERROR_MSG)
        res = user_dao.update_user_role(user['id'], new_role_id=role_id)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)    
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.UPDATE_USER_ERROR_MSG)

    def delete_user(self,user_nickname:str):
        user = user_dao.get_user_by_nickname(user_nickname)
        if not user:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.USER_DOES_NOT_EXISTS_ERROR_MSG)
        res = user_dao.delete_user(user['id'])
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)    
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_USER_ERROR_MSG)        

    def get_all_users(self):
        users = user_dao.get_all_users()
        if not users:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.GET_ALL_USERS_ERROR_MSG)        
        return create_response(StatusCodes.STATUS_OK,data=users)
        
    def _encrypt_password(self,input_password:str) -> bytes:
        return bcrypt.hashpw(input_password.encode("utf-8"), bcrypt.gensalt())

    def _check_password(self,input_password: str,hashed_password) -> bool:
        return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)
    