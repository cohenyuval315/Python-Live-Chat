from sqlalchemy.orm import DeclarativeBase,DeclarativeMeta

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    
    
class BaseMetaModel(Base):
    __abstract__ = True