from prompt_python_chat.config import app_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,registry
from aiohttp import web
from prompt_python_chat.db_models import BaseModel
from prompt_python_chat.metadata import MetaData



engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI,echo=app_config.SQLALCHEMY_ECHO,logging_name=app_config.LEVEL)
Session = sessionmaker(autocommit=app_config.SQL_ALCHEMY_SESSION_AUTO_COMMIT,autoflush=app_config.SQL_ALCHEMY_SESSION_AUTO_FLUSH,expire_on_commit=app_config.SQL_ALCHEMY_EXPIRE_ON_COMMIT,bind=engine)

metadata_obj = MetaData(Session())

async def init_db(app: web.Application):
    _registry = registry()
    _registry.configure()

    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    metadata_obj.init_data()
    app['engine'] = engine