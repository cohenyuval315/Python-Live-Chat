import os
from dotenv import load_dotenv
import enum

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

APP_NAME = "test"
LEVEL = "DEBUG"

class config():
    APP_NAME = "test"
    LEVEL = "DEBUG"

    HOST = os.environ.get('HOST')   
    PORT = os.environ.get('PORT')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_PEM_PATH = '/path/to/server.pem'
    SERVER_KEY_PATH = '/path/to/server.key'
    DB_SYSTEM = os.environ.get('DB_SYSTEM')
    DB_SYSTEM_CONNECTOR = os.environ.get('DB_SYSTEM_CONNECTOR')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')  

class DevConfig(config):
    DEV_DB_NAME = "dev.db"
    SQLITE_PREFIX = "sqlite:///"
    SQL_ALCHEMY_SESSION_AUTO_COMMIT = False
    SQL_ALCHEMY_SESSION_AUTO_FLUSH=False
    SQL_ALCHEMY_EXPIRE_ON_COMMIT= False    
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX+ os.path.join(BASE_DIR,DEV_DB_NAME)      # SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    SQLITE_MEMORY_URI = "sqlite+pysqlite:///:memory:"
    SQLALCHEMY_DATABASE_PEM = os.environ.get("SQLALCHEMY_DATABASE_PEM")
    SQLALCHEMY_ECHO= True
    SQLALCHEMY_TRACK_MODIFICATIONS= True

  
class TestConfig(config):
    pass

class ProdConfig(config):
    pass


app_config = DevConfig()


class globals(enum.Enum):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_NAME = "prompt chat"
    LOG_LEVEL = "DEBUG"
    CONFIG = DevConfig()