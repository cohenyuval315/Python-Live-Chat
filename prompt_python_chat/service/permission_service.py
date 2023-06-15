from .base_service import BaseService
from prompt_python_chat.constants import BlockType,RoleType
from prompt_python_chat.db_dao import permission_dao,role_dao,block_dao
from prompt_python_chat.constants import StatusCodes,Errors
from typing import Optional
from prompt_python_chat.utils import decode_token,generate_access_token,generate_refresh_token,create_response

class PermissionsService(BaseService):

    def __init__(self,secret_key) -> None:
        super().__init__()
        self.secret_key = secret_key

    def get_role_by_role_type(self,role_type:RoleType):
        res = role_dao.get_role_by_name(role_type)
        if res:
            return create_response(StatusCodes.STATUS_OK,data=res)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.NO_ROLE_ERROR_MSG)


    def get_role_by_id(self,role_id:int) -> Optional[dict]:
        role = role_dao.get_role_by_id(role_id)
        if role:
            return create_response(StatusCodes.STATUS_OK,data=role)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.NO_ROLE_ERROR_MSG)

    def has_permissions_by_role(self,role_id:int,permmited_role_id:int):
        _role = role_dao.get_role_object_by_id(role_id)
        _permmited_role = role_dao.get_role_object_by_id(permmited_role_id)
        if not _role or not _permmited_role:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.NO_ROLE_ERROR_MSG)
        
        is_grant = role_dao.is_role_child_of_permmited_role(_role,_permmited_role)
        if is_grant:
            return create_response(StatusCodes.STATUS_OK,data={})
        return create_response(StatusCodes.STATUS_UNAUTHORIZED,Errors.UNAUTH)
        
    def has_permissions_by_permission_name(self,role_id:int, permission_name:str):
        role_permission = permission_dao.get_permission_by_name(permission_name)
        if not role_permission:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.NO_PERMISSION_ERROR_MSG)
        role = self.get_role_by_id(role_id)
        if not role:
            return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.NO_ROLE_ERROR_MSG)
        is_granted = self.has_permissions_by_role(role['id'],role_permission['id'])
        if is_granted:
            return create_response(StatusCodes.STATUS_OK,data={})
        return create_response(StatusCodes.STATUS_UNAUTHORIZED,Errors.UNAUTH)
        
    def get_user_block_status(self,channel_id:int,user_id:int):
        blocks = block_dao.get_blocks_by_channel_and_user(channel_id=channel_id,user_id=user_id)
        if len(blocks) == 0:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.BLOCK_DOES_NOT_EXISTS_ERROR_MSG)
        res = {}
        for block in blocks:
            block_type_name = block['type']
            res[block_type_name] = True
        return create_response(StatusCodes.STATUS_OK,data=res)
        
    def block_user(self,channel_id:int,user_id:int,block_type:BlockType):
        blocks = block_dao.get_blocks_by_channel_and_user(user_id,channel_id)
        for block in blocks:
            if block['type'] == block_type.value:
                return create_response(StatusCodes.STATUS_CONFLIC,Errors.BLOCK_EXISTS_ERROR_MSG)
        new_block = block_dao.create_block(channel_id,user_id,block_type)
        if new_block:
            return create_response(StatusCodes.STATUS_CREATED,data=new_block)
        return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.CREATE_BLOCK_ERROR_MSG)

    def unblock_user(self,user_id:int,channel_id:int):
        blocks = block_dao.get_block_objects_by_channel_and_user(channel_id,user_id)
        if len(blocks) == 0:
            return create_response(StatusCodes.STATUS_NOT_FOUND,Errors.BLOCK_DOES_NOT_EXISTS_ERROR_MSG)
        deleted_blocks_ids = []
        for block in blocks:
            deleted = block_dao.delete_block(block)
            if not deleted:
                return create_response(StatusCodes.STATUS_INTERNAL_SERVER_ERROR,Errors.DELETE_BLOCK_ERROR_MSG)
            deleted_blocks_ids.append(deleted)
        return create_response(StatusCodes.STATUS_OK,data=deleted_blocks_ids)








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
