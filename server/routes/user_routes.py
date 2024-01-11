from aiohttp import web
from constants import Endpoints
from controllers.user_controller import UserController

user_routes = web.RouteTableDef()

@user_routes.post(Endpoints.PUT_PROMOTE_USER.value)
async def promote_user(request: web.Request) -> web.Response:
    return await UserController.promote_user(request)


@user_routes.post(Endpoints.PUT_DEMOTE_USER.value)
async def demote_user(request: web.Request) -> web.Response:
    return await UserController.demote_user(request)


@user_routes.delete(Endpoints.DELETE_UNBLOCK_USER.value)
async def unblock_user(request: web.Request) -> web.Response:
    return await UserController.unblock_user(request)


@user_routes.get(Endpoints.GET_ALL_USERS.value)
async def get_all_users(request: web.Request) -> web.Response:
    return await UserController.get_all_users(request)


@user_routes.put(Endpoints.POST_READ_ONLY_USER.value)
async def ban_user(request: web.Request) -> web.Response:
    return await UserController.ban_user(request)


@user_routes.put(Endpoints.POST_BAN_USER.value)
async def silence_user(request: web.Request) -> web.Response:
    return await UserController.silence_user(request)


@user_routes.delete(Endpoints.DELETE_USER.value)
async def delete_user(request: web.Request) -> web.Response:
    return await UserController.delete_user(request)
