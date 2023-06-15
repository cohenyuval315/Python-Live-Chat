from typing import Optional,List
from prompt_python_chat.db_models import User
from .base_dao import BaseDao
from sqlalchemy import select


class UserDao(BaseDao):

    def _return_user(self,user:User) -> dict:
        return {
            "id" : user.id,
            "username": user.username,
            "nickname": user.nickname,
            "password": user.password,
            "role_id": user.role_id,
        }

    def is_username_exists(self, username: str) -> bool:
        if self.get_session().query(User).filter_by(username=username).first():
            return True
        return False

    def is_nickname_exists(self,nickname: str) -> bool:
        if self.get_session().query(User).filter_by(nickname=nickname).first():
            return True
        return False

    def get_user_object_by_id(self,user_id:int) -> Optional[User]:
        return self.get_session().scalars(select(User).where(User.id == user_id)).one_or_none()

    def get_user_by_id(self,user_id:int) -> Optional[dict]:
        user = self.get_user_object_by_id(user_id)
        if user:
            return self._return_user(user)

    def get_user_object_by_nickname(self,nickname:str) -> Optional[User]:
        return self.get_session().scalars(select(User).where(User.nickname == nickname)).one_or_none()
    
    def get_user_by_nickname(self,nickname: str) -> Optional[dict]:
        user =  self.get_user_object_by_nickname(nickname)
        if user:
            return self._return_user(user) 

    def get_user_object_by_username(self,username:str) -> Optional[User]:
        return self.get_session().scalars(select(User).where(User.username == username)).one_or_none()
        
    def get_user_by_username(self,username: str) -> Optional[dict]:
        user = self.get_user_object_by_username(username)
        if user:
            return self._return_user(user)        

    def create_user_object(self,nickname: str,username: str,password: bytes , role_id:int) -> Optional[User]:
        user_id = self.generate_id()
        user = User(id=user_id,username=username,nickname=nickname,password=password,role_id=role_id)
        self.get_session().add(user)
        self.get_session().commit()
        new_user = self.get_user_object_by_id(user_id)
        if new_user:
            return new_user
            
    def create_user(self,nickname: str,username: str,password: bytes , role_id:int) -> Optional[dict]:
        user = self.create_user_object(nickname,username,password,role_id)
        if user:
            return self._return_user(user)

    def update_user_object_role(self,user_id:int, new_role_id:int) -> Optional[User]:
        user = self.get_user_object_by_id(user_id)
        if user:
            user.role_id = new_role_id
            self.get_session().commit()
            return user
 
    def update_user_role(self,user_id:int, new_role_id:int) -> Optional[dict]:
        user = self.update_user_object_role(user_id,new_role_id)
        if user:
            return self._return_user(user)
        
    def delete_user_object(self,user:User) -> Optional[dict]:
        self.get_session().delete(user)
        self.get_session().commit()
        deleted_user_id = user.id
        deleted_user = self.get_user_by_id(deleted_user_id)
        if not deleted_user:
            return {"user_id":deleted_user_id}
        return {}

    def get_delete_user_object(self,user:User) -> Optional[User]:
        self.get_session().delete(user)
        self.get_session().commit()
        deleted_user_id = user.id
        deleted_user = self.get_user_by_id(deleted_user_id)
        if not deleted_user:
            return user

    def get_delete_user(self,user_id:int) -> Optional[dict]:
        user = self.get_user_object_by_id(user_id)
        if user:
            deleted_user = self.get_delete_user_object(user)
            if deleted_user:
                return self._return_user(deleted_user)
        
    def delete_user(self,user_id:int) -> Optional[dict]:
        user = self.get_user_object_by_id(user_id)
        if user:
            return self.delete_user_object(user)
        
    def get_all_users_objects(self) -> List[User]:
        return list(self.get_session().scalars(select(User)).all())

    def get_all_users(self) -> List[dict]:
        users = []
        for user in self.get_session().scalars(select(User)).all():
            users.append(self._return_user(user))
        return users


user_dao = UserDao()