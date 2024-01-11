from .base_service import BaseService
from typing import Optional
import bcrypt
from db_dao import user_dao
from uuid import uuid4 as v4
from exceptions import InternalServerError,AlreadyExistsError,DoesNotExistsError

class UsersService(BaseService):
    GUEST_ANONYMOUS = "anon"
    GUEST_NUMBER_LENGTH=6

    def get_user_by_id(self,user_id:int):
        res =  user_dao.get_user_by_id(user_id)
        if res:
            return res
        else:
            raise DoesNotExistsError('User does not exists')

    def login_user(self,username: str,password: str) -> Optional[dict]:
        if not user_dao.is_username_exists(username):
            raise DoesNotExistsError('Username does not exists')
        user = user_dao.get_user_by_username(username)
        if not user:
            raise InternalServerError('login_user, internal error')
        if self._check_password(password,user['password']):
            return user
        else:
            raise DoesNotExistsError('Wrong password')
    
    def login_guest(self):
        guest_id = int(str(v4().int)[:self.GUEST_NUMBER_LENGTH])
        nickname = self.GUEST_ANONYMOUS + "_" + str(guest_id)
        guest_data = {
            "id":guest_id,
            "nickname":nickname
        }
        return guest_data


    def create_user(self,nickname:str,username:str,password:str,role_id:int):
        if user_dao.is_username_exists(username):
            raise AlreadyExistsError('username already exists')
        if user_dao.is_nickname_exists(nickname):
            raise AlreadyExistsError('nickname already exists')
        res = user_dao.create_user(nickname,username,self._encrypt_password(password),role_id=role_id)
        if res:
            return res
        raise InternalServerError('create_user internal error')
        
   
    def update_user_role(self,user_nickname:str,role_id:int):
        user = user_dao.get_user_by_nickname(user_nickname)
        if not user:
            raise DoesNotExistsError('User does not exists')
        res = user_dao.update_user_role(user['id'], new_role_id=role_id)
        if res:
            return res
        raise InternalServerError('update_user_role internal error')

    def delete_user(self,user_nickname:str):
        user = user_dao.get_user_by_nickname(user_nickname)
        if not user:
            raise DoesNotExistsError('User does not exists')
        res = user_dao.delete_user(user['id'])
        if res:
            return res
        raise InternalServerError('delete_user internal error')
        

    def get_all_users(self):
        users = user_dao.get_all_users()
        if users:
            return users
        raise InternalServerError('get_all_users internal error')
        
    def _encrypt_password(self,input_password:str) -> bytes:
        return bcrypt.hashpw(input_password.encode("utf-8"), bcrypt.gensalt())

    def _check_password(self,input_password: str,hashed_password:str) -> bool:
        return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password.encode("utf-8"))
    