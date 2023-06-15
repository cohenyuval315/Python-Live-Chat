from aiohttp import web
from prompt_python_chat.constants import Endpoints
from prompt_python_chat.controllers.auth_controller import AuthController
auth_routes = web.RouteTableDef()


@auth_routes.post(Endpoints.POST_SIGNUP.value)
async def sign_up(request: web.Request) -> web.Response:
    return await AuthController.sign_up(request)

@auth_routes.post(Endpoints.POST_LOGIN_GUEST.value)
async def login_guest(request: web.Request) -> web.Response:
    return await AuthController.login_guest(request)

@auth_routes.post(Endpoints.POST_LOGIN.value)
async def login(request: web.Request) -> web.Response:
    return await AuthController.login_user(request)

@auth_routes.post(Endpoints.POST_LOGOUT.value)
async def logout(request: web.Request) -> web.Response:
    return await AuthController.logout_user(request)

@auth_routes.post(Endpoints.GET_REFRESH_TOKEN.value)
async def get_refresh_token(request:web.Request):
    return await AuthController.refresh_access_token(request)