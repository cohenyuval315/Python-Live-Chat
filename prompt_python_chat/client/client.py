from contextlib import asynccontextmanager
import functools
import dataclasses
from typing import Any, AsyncIterator, Awaitable, Callable
import asyncio
from yarl import URL
import click
from prompt_python_chat.client.client_config import config
from  prompt_python_chat.client.snack_client import SnackChatClient


@dataclasses.dataclass()
class Root:
    base_url: URL
    show_traceback: bool
    
    @asynccontextmanager
    async def client(self) -> AsyncIterator[SnackChatClient]:
        _client = SnackChatClient(self.base_url)
        yield _client
            


def async_cmd(func: Callable[..., Awaitable[None]]) -> Callable[..., None]:
    @functools.wraps(func)
    def inner(root: Root, **kwargs: Any) -> None:
        try:
            coro = func(root, **kwargs)
            return asyncio.run(coro) # type: ignore
        except Exception as exc:
            if root.show_traceback:
                raise
            else:
                click.echo(f"Error: {exc}")

    inner = click.pass_obj(inner)
    return inner




@click.group()
@click.option(
    "--base-url", type=str, default=f"http://{config.HOST}:{config.PORT}", show_default=True
)
@click.option("--show-traceback", is_flag=True, default=False, show_default=True)
@click.pass_context
def main(ctx: click.Context, base_url: str, show_traceback: bool) -> None:
    ctx.obj = Root(URL(base_url), show_traceback)



@main.command()
@click.option("--nickname", type=str, required=True)
@click.option("--username", type=str, required=True)
@click.option("--password", type=str, required=True)
@async_cmd
async def sign_up(root: Root,nickname:str, username: str, password: str) -> None:
    """Create new user"""
    async with root.client() as client:
        await client.init(nickname=nickname ,username=username, password=password)


@main.command()
@click.option("--username", type=str, required=True)
@click.option("--password", type=str, required=True)
@async_cmd
async def login(root: Root, username: str, password:str) -> None:
    """login user"""
    async with root.client() as client:
        await client.init(username=username,password=password)


@main.command()
@async_cmd
async def guest(root: Root) -> None:
    """connect as guest"""
    async with root.client() as client:
        await client.init()


if __name__ == '__main__':
    main()
