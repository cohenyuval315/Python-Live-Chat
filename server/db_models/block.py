from .base import BaseModel
from sqlalchemy import Enum
from constants import BlockType
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column


class Block(BaseModel):
    __tablename__ = 'block'
    id:Mapped[int] = mapped_column(primary_key=True,unique=True,nullable=False)
    channel_id:Mapped[int] = mapped_column(nullable=False)
    user_id:Mapped[int] = mapped_column(nullable=False)
    block_type:Mapped[BlockType] = mapped_column(Enum(BlockType),default=BlockType.READONLY,nullable=False)
    timestamp:Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Block: type:{self.block_type.value} user_id: {self.user_id} channel_id:{self.channel_id}"
    

    
