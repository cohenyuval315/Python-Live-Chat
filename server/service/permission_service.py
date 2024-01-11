from .base_service import BaseService
from constants import BlockType,RoleType
from db_dao import permission_dao,role_dao,block_dao
from typing import Optional
from utils import decode_token,generate_access_token,generate_refresh_token
from exceptions import AlreadyExistsError, DoesNotExistsError, InternalServerError
class PermissionsService(BaseService):

    def __init__(self,secret_key) -> None:
        super().__init__()
        self.secret_key = secret_key

    def get_role_by_role_type(self,role_type:RoleType):
        res = role_dao.get_role_by_name(role_type)
        if res:
            return res
        raise InternalServerError('get_role_by_role_type internal error')


    def get_role_by_id(self,role_id:int) -> Optional[dict]:
        role = role_dao.get_role_by_id(role_id)
        if role:
            return role
        raise InternalServerError('get_role_by_id internal error')

    def has_permissions_by_role(self,role_id:int,permmited_role_id:int):
        if role_id == permmited_role_id:
            return True
        _role = role_dao.get_role_object_by_id(role_id)
        _permmited_role = role_dao.get_role_object_by_id(permmited_role_id)
        
        if _role and _permmited_role:
            is_grant = role_dao.is_role_child_of_permmited_role(_role,_permmited_role)
            if is_grant:
                return True
            else:
                return False
        else:
            raise InternalServerError('has_permissions_by_role internal error')

        
        
    def has_permissions_by_permission_name(self,role_id:int, permission_name:str):
        role_permission = permission_dao.get_permission_by_name(permission_name)
        if not role_permission:
            raise InternalServerError('role_permission internal error')
        role = self.get_role_by_id(role_id)
        if not role:
            raise InternalServerError('role_permission internal error')
        is_granted = self.has_permissions_by_role(role['id'],role_permission['id'])
        if is_granted:
            return True
        return False
        
    def get_user_block_status(self,channel_id:int,user_id:int):
        blocks = block_dao.get_blocks_by_channel_and_user(channel_id=channel_id,user_id=user_id)
        if len(blocks) == 0:
            raise DoesNotExistsError('block does not exists')
        res = {}
        for block in blocks:
            block_type_name = block['type']
            res[block_type_name] = True
        return res
        
    def block_user(self,channel_id:int,user_id:int,block_type:BlockType):
        blocks = block_dao.get_blocks_by_channel_and_user(user_id,channel_id)
        for block in blocks:
            if block['type'] == block_type.value:
                raise AlreadyExistsError('block already exists')
        new_block = block_dao.create_block(channel_id,user_id,block_type)
        if new_block:
            return new_block
        raise InternalServerError('block_user internal error')

    def unblock_user(self,user_id:int,channel_id:int):
        blocks = block_dao.get_block_objects_by_channel_and_user(channel_id,user_id)
        if len(blocks) == 0:
            raise DoesNotExistsError('block does not exists')
        deleted_blocks_ids = []
        for block in blocks:
            deleted = block_dao.delete_block(block)
            if not deleted:
                raise InternalServerError('unblock_user internal error')
            deleted_blocks_ids.append(deleted)
        return deleted_blocks_ids








    def decode_user_token(self,access_token):
        return decode_token(access_token,self.secret_key)

    def generate_user_access_token(self,user_id:int):
        access_token = generate_access_token(user_id,self.secret_key)
        return access_token

    def generate_user_refresh_token(self,user_id:int):
        refresh_token = generate_refresh_token(user_id,self.secret_key)
        return refresh_token

    def refresh_user_token(self,user_id:int):
        return self.generate_user_access_token(user_id)
