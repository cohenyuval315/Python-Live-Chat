from .base import BaseModel
from constants import RoleType,ColorType
from sqlalchemy import ForeignKey,Enum
from sqlalchemy.orm import relationship,Mapped,mapped_column

class Role(BaseModel):
    __tablename__ = "role"
    id:Mapped[int] = mapped_column(primary_key=True,unique=True,nullable=False)
    name:Mapped[RoleType] = mapped_column(Enum(RoleType),primary_key=True,unique=True,nullable=False)
    color:Mapped[ColorType] = mapped_column(Enum(ColorType),primary_key=True,unique=True,nullable=False)
    child_role_id:Mapped[int] = mapped_column(ForeignKey('role.id'),nullable=True)
    child_role:Mapped['Role'] = relationship()

    def __repr__(self) -> str:
        return f"Role: id:{self.id} name:{self.name}"
    