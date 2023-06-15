from aiohttp import web
from prompt_python_chat.routes import auth_routes,channel_routes,user_routes
from prompt_python_chat.config import app_config
from prompt_python_chat.service.messages_service import MessagesService
from prompt_python_chat.service.online_service import OnlineService
from prompt_python_chat.service.permission_service import PermissionsService
from prompt_python_chat.service.user_service import UsersService
import click
import dataclasses
from prompt_python_chat.exts import init_db
import ssl

async def init_app() -> web.Application:
    app = web.Application()
    await init_db(app)
    app.add_routes(auth_routes)
    app.add_routes(channel_routes)
    app.add_routes(user_routes)
    
    messages_service = MessagesService()
    online_service = OnlineService()
    permissions_service = PermissionsService(app_config.SECRET_KEY)
    users_service = UsersService()
    online_service._set_channels(messages_service._get_all_channels()['data'])

    app["messages_service"] = messages_service
    app["online_service"] = online_service
    app['permissions_service'] = permissions_service
    app['users_service'] = users_service
    return app


def init(host:str,port:int):
    # ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain(app_config.SERVER_PEM_PATH,app_config.SERVER_KEY_PATH)

    web.run_app(init_app(), host=host,port=port)#,ssl_context=ssl_context)


@dataclasses.dataclass(frozen=True)
class Serve:
    host: str
    port: str
    show_traceback: bool

@click.group()
@click.option("--host", type=str, default=f"{app_config.HOST}", show_default=True)
@click.option("--port", type=str, default=f"{app_config.PORT}", show_default=True)
@click.option("--show-traceback", is_flag=True, default=False, show_default=True)
@click.pass_context
def main(ctx: click.Context,host: str, port:str , show_traceback: bool) -> None:
    ctx.obj = Serve(host,port, show_traceback)
    
    
@main.command()
@click.pass_context
def start(ctx: click.Context) -> None:
    """start server"""
    serve = ctx.obj
    init(serve.host, int(serve.port))


if __name__ == '__main__':
    main()
    
