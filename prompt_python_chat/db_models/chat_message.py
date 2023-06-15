from .base import BaseModel
from sqlalchemy import ForeignKey,Text
from datetime import datetime
from sqlalchemy import ForeignKey,Text,Enum
from sqlalchemy.orm import Mapped,mapped_column
from prompt_python_chat.constants import ColorType



class ChatMessage(BaseModel):
    __tablename__ = "chat_message"
    id:Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    channel_id:Mapped[int] = mapped_column(ForeignKey("channel.id"),nullable=False)
    channel_msg_index:Mapped[int] = mapped_column(nullable=False,autoincrement=True,default=0)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),nullable=False)
    nickname:Mapped[str] = mapped_column(ForeignKey('user.nickname'),nullable=False)
    content:Mapped[Text] = mapped_column(Text(30),nullable=False)
    timestamp:Mapped[datetime] = mapped_column(default=datetime.utcnow)
    color:Mapped[ColorType]= mapped_column(Enum(ColorType), nullable=False)
    

    def __repr__(self) -> str:
        return f"Chat Message: user:{self.nickname} content:{self.content} channel_id:{self.channel_id} channel index: {self.channel_msg_index}"
    