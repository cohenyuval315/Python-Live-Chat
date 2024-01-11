from .base_dao import BaseDao
from db_models import Permission
from typing import Optional
from sqlalchemy import select

class PermissionDao(BaseDao):

    def _return_permission(self,permission:Permission) -> dict:
        return {
            "id": permission.id,
            "name" : permission.name,
            "require_target" :permission.require_target,
            "role_id" : permission.role_id
        }
    
    def get_permission_object_by_id(self,permission_id:int) -> Optional[Permission]:
        return self.get_session().execute(select(Permission).filter_by(permission_id=permission_id)).scalar_one_or_none()

    def get_permission_by_id(self,permission_id:int) -> Optional[dict]:
        _permission = self.get_permission_object_by_id(permission_id)
        if _permission:
            self._return_permission(_permission)

    def get_permission_object_by_name(self,permission_name:str) -> Optional[Permission]:
        return self.get_session().execute(select(Permission).filter_by(name=permission_name)).scalar_one_or_none()

    def get_permission_by_name(self,permission_name:str) -> Optional[dict]:
        _permisson = self.get_permission_object_by_name(permission_name)
        if _permisson:
            return self._return_permission(_permisson)

    

permission_dao = PermissionDao()