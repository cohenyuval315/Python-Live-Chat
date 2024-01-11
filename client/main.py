from contextlib import asynccontextmanager
import functools
import dataclasses
from typing import Any, AsyncIterator, Awaitable, Callable
import asyncio
import click
from snack_app import SnackChatClient
from logger import logger
@dataclasses.dataclass()
class Root:    
    @asynccontextmanager
    async def client(self) -> AsyncIterator[SnackChatClient]:
        _client = SnackChatClient()
        yield _client
            


def async_cmd(func: Callable[..., Awaitable[None]]) -> Callable[..., None]:
    @functools.wraps(func)
    def inner(root: Root, **kwargs: Any) -> None:
        try:
            coro = func(root, **kwargs)
            return asyncio.run(coro) # type: ignore
        except Exception as exc:
            logger.error(f"An error occurred: {exc}", exc_info=True)


    inner = click.pass_obj(inner)
    return inner




@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.obj = Root()



@main.command()
@click.option("--nickname", type=str, required=True)
@click.option("--username", type=str, required=True)
@click.option("--password", type=str, required=True)
@async_cmd
async def sign_up(root: Root,nickname:str, username: str, password: str) -> None:
    """Create new user"""
    try:
        async with root.client() as client:
            await client.init(nickname=nickname ,username=username, password=password)
    except Exception as e:
        logger.error(e)


@main.command()
@click.option("--username", type=str, required=True)
@click.option("--password", type=str, required=True)
@async_cmd
async def login(root: Root, username: str, password:str) -> None:
    """login user"""
    try:
        async with root.client() as client:
            await client.init(username=username,password=password)
    except Exception as e:
        logger.error(e)

@main.command()
@async_cmd
async def guest(root: Root) -> None:
    """connect as guest"""
    try:
        async with root.client() as client:
            await client.init()
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()
