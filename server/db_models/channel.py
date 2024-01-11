from .base import BaseModel
from sqlalchemy import String,ForeignKey,Enum
from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column
from constants import ColorType

class Channel(BaseModel):
    __tablename__ = "channel"
    id:Mapped[int] = mapped_column(primary_key=True,unique=True,nullable=False)
    name:Mapped[str] = mapped_column(String(30),primary_key=True,unique=True,nullable=False)
    role_id:Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False)
    color:Mapped[ColorType]= mapped_column(Enum(ColorType), nullable=False)

    def __repr__(self) -> str:
        return f"Channel: name:{self.name} role_id:{self.role_id} color:{self.color}"
        