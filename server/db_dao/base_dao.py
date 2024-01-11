from exts import Session
from uuid import uuid4 as v4
from sqlalchemy.exc import SQLAlchemyError

class BaseDao:
    ID_LEN = 9


    def __init__(self):
        self.session = None
    
    def __enter__(self):
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()
    
    def get_session(self):
        if self.session is None:
            self.session = Session()
        return self.session

    def commit(self):
        if self.session is not None:
            self.session.commit()

    def rollback(self):
        if self.session is not None:
            self.session.rollback()
            
    def close(self):
        if self.session is not None:
            self.session.close()

    def generate_id(self):
        return int(str(v4().int)[:self.ID_LEN])

