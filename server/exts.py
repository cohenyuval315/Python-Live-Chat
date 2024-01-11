from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,registry
from aiohttp import web
from db_models import BaseModel
from db_seed import Seed
import os
import logging
from logger import logger

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def create_connection_string(useSqllite=False,memory=False):
    if useSqllite:
        if memory:
            SQLITE_MEMORY_URI = "sqlite+pysqlite:///:memory:"
            return SQLITE_MEMORY_URI
        else:
            SQLALCHEMY_SQLLITE_DB_PATH = os.environ.get('SQLALCHEMY_SQLLITE_DB_PATH')
            return f"sqlite:///{os.path.join(BASE_DIR,SQLALCHEMY_SQLLITE_DB_PATH)}"
    else:
        DB_SYSTEM = os.environ.get('DB_SYSTEM')
        DB_SYSTEM_CONNECTOR = os.environ.get('DB_SYSTEM_CONNECTOR')
        DB_USER = os.environ.get('DB_USER')
        DB_PASS = os.environ.get('DB_PASS')
        DB_HOST = os.environ.get('DB_HOST')
        DB_PORT = os.environ.get('DB_PORT')
        DB_NAME = os.environ.get('DB_NAME')
        return (
            f"{DB_SYSTEM}+{DB_SYSTEM_CONNECTOR}://"
            f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        


SQLALCHEMY_LOG_LEVEL = os.environ.get('SQLALCHEMY_LOG_LEVEL',logging.DEBUG)
SQL_ALCHEMY_SESSION_AUTO_COMMIT = os.environ.get('SQL_ALCHEMY_SESSION_AUTO_COMMIT',False) == 'true'
SQL_ALCHEMY_SESSION_AUTO_FLUSH = os.environ.get('SQL_ALCHEMY_SESSION_AUTO_FLUSH',False) == 'true'
SQL_ALCHEMY_EXPIRE_ON_COMMIT = os.environ.get('SQL_ALCHEMY_EXPIRE_ON_COMMIT',False) == 'true'
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO',False) == 'true'
USE_SQLLITE = os.environ.get('USE_SQLLITE',True) == 'true'
USE_MEMORY = os.environ.get('USE_MEMORY',False) == 'true'
CREATE_DB = os.environ.get('CREATE_DB',False) == 'true'
SQLALCHEMY_DATABASE_URI = create_connection_string(USE_SQLLITE,USE_MEMORY)
logger.info('Database URI: {}...'.format(SQLALCHEMY_DATABASE_URI))
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       echo=SQLALCHEMY_ECHO,
                       logging_name=SQLALCHEMY_LOG_LEVEL)
Session = sessionmaker(autoflush=SQL_ALCHEMY_SESSION_AUTO_FLUSH,
                       expire_on_commit=SQL_ALCHEMY_EXPIRE_ON_COMMIT,
                       bind=engine)

seed_data = Seed(Session())

async def init_db(app: web.Application):
    
    _registry = registry()
    _registry.configure()

    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    seed_data.init_data()
    app['engine'] = engine