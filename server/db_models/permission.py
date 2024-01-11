from .base import BaseModel
from sqlalchemy import String,ForeignKey
from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column

class Permission(BaseModel):
    __tablename__ = 'permissions'
    id:Mapped[int] = mapped_column(primary_key=True,unique=True,nullable=False)
    name:Mapped[str] = mapped_column(String(30),primary_key=True,unique=True,nullable=False)
    require_target:Mapped[bool] = mapped_column(default=False)
    role_id:Mapped[int] = mapped_column(ForeignKey("role.id"))

    def __repr__(self) -> str:
        return f"Permission : name:{self.name} role_id:{self.role_id}"
