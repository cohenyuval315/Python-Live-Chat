from typing import Optional
from prompt_python_chat.db_models import Block
from prompt_python_chat.constants import BlockType
from .base_dao import BaseDao
from sqlalchemy import select
from typing import List

class BlockDao(BaseDao):

    def _return_block(self,block:Block):
        return {
            "id":block.id,
            "channel_id":block.channel_id,
            "user_id":block.user_id,
            "type":block.block_type,
            "timestamp":block.timestamp
        }

    def get_block_object_by_id(self,block_id:int) -> Optional[Block]:
        return self.get_session().execute(select(Block).filter_by(id=block_id)).scalar_one_or_none()

    def get_block_by_id(self,block_id:int) -> Optional[dict]:
            _block = self.get_block_object_by_id(block_id)
            if _block:
                return self._return_block(_block)

    def get_block_objects_by_channel_and_user(self,channel_id:int, user_id:int) -> List[Block]:
        return list(self.get_session().scalars(select(Block).filter_by(channel_id=channel_id).filter_by(user_id=user_id)).all())

    def get_blocks_by_channel_and_user(self,channel_id:int, user_id:int) -> List[dict]:
        _blocks = self.get_block_objects_by_channel_and_user(channel_id,user_id)
        return [self._return_block(block) for block in _blocks]

    def create_block_object(self,channel_id:int,user_id:int,block_type:BlockType) -> Optional[Block]:
        block_id = self.generate_id()
        new_block = Block(id=block_id,channel_id=channel_id,block_type=block_type,blocked_user_id=user_id)
        self.get_session().add(new_block)
        self.get_session().commit()
        self.get_block_by_id(block_id)
        _block = self.get_block_object_by_id(block_id)
        if _block:
            return new_block        

    def create_block(self,channel_id:int,user_id:int,block_type:BlockType) -> Optional[dict]:
        _block = self.create_block_object(channel_id,user_id,block_type)
        if _block:
            return self._return_block(_block)

    def delete_block(self,block:Block) -> Optional[dict]:
        deleted_block = self.get_delete_block_object(block)
        if deleted_block:
            return {"block_id":deleted_block.id}

    def get_delete_block_object(self,block:Block) -> Optional[Block]:
        self.get_session().delete(block)
        self.get_session().commit()
        delete_block_id = block.id
        delete_block = self.get_block_object_by_id(delete_block_id)
        if not delete_block:
            return block
        
    def delete_blocks_by_channel_id_user_id(self,user_id:int,channel_id:int) -> List[dict]:
        blocks = self.get_block_objects_by_channel_and_user(channel_id,user_id)
        deleted_blocks = []
        for block in blocks:
            deleted_block = self.delete_block(block)
            deleted_blocks.append(deleted_block)
        return deleted_blocks
        
    def is_block_exists(self,block_id:int) -> bool:
        if self.get_block_object_by_id(block_id):
            return True
        return False


block_dao = BlockDao()
