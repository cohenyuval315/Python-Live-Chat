from .base_dao import BaseDao
from db_models import Role
from constants import RoleType
from typing import Optional
from sqlalchemy import select

class RoleDao(BaseDao):

    def _return_role(self,role:Role) -> dict:
        return {
            "id":role.id,
            "name":role.name.value,
            "color":role.color.value
        }

    def get_role_object_by_id(self,role_id:int) -> Optional[Role]:
        return self.get_session().execute(select(Role).filter_by(id=role_id)).scalar_one_or_none()

    def get_role_by_id(self,role_id:int) -> Optional[dict]:
        _role = self.get_role_object_by_id(role_id)
        if _role:
            return self._return_role(_role)

    def get_role_object_by_name(self,role_name:RoleType) -> Optional[Role]:
        return self.get_session().execute(select(Role).filter_by(name=role_name.value)).scalar_one_or_none()

    def get_role_by_name(self,role_name:RoleType) -> Optional[dict]:
        _role = self.get_role_object_by_name(role_name)
        if _role:
            return self._return_role(_role)

    def has_permissions(self,role:RoleType ,permitted_role:RoleType) -> Optional[bool]:
        _role = self.get_role_object_by_name(role)
        _permmited_role = self.get_role_object_by_name(permitted_role)

        if _role and _permmited_role:
            if _role.id == _permmited_role.id:
                return True
            return not self.is_role_child_of_permmited_role(_role,_permmited_role)
    
    def is_role_child_of_permmited_role(self,role:Role,permmited_role:Role):
        if role.id == permmited_role.id:
            return True
        child_roles = self.get_session().execute(select(Role).filter_by(child_role_id=role.id)).scalars().all()
        return any(self.is_role_child_of_permmited_role(child_role,permmited_role) for child_role in child_roles)
        
role_dao = RoleDao()