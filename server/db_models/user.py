from .base import BaseModel
from sqlalchemy import ForeignKey,String,Text
from sqlalchemy.orm import relationship,Mapped,mapped_column
from .role import Role


class User(BaseModel):
    __tablename__ = "user"
    id:Mapped[int] = mapped_column(primary_key=True,unique=True,nullable=False)
    username:Mapped[str] = mapped_column(String(30),primary_key=True,unique=True,nullable=False)
    nickname:Mapped[str] = mapped_column(String(30),primary_key=True,unique=True,nullable=False)
    password:Mapped[Text] = mapped_column(Text,nullable=False)
    role_id:Mapped[int] = mapped_column(ForeignKey("role.id"),nullable=False)
    role: Mapped["Role"] = relationship()


    def __repr__(self) -> str:
        return f"User: username:{self.username} nick:{self.nickname} role_id:{self.role_id}"
    
