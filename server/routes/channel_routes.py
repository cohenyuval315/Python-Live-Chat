from aiohttp import web
from constants import Endpoints
from controllers.channel_controller import ChannelController

channel_routes = web.RouteTableDef()

@channel_routes.post(Endpoints.POST_MESSAGE.value)
async def post_message(request:web.Request):
    return await ChannelController.post_message(request)


@channel_routes.get(Endpoints.GET_CHANNEL_MESSAGES.value)
async def get_channel_messages(request):
    return await ChannelController.get_channel_messages(request)

@channel_routes.post(Endpoints.CHANGE_CHANNEL.value)
async def change_channel(request: web.Request) -> web.Response:
    return await ChannelController.change_channel(request)

@channel_routes.post(Endpoints.EXIT_CHANNEL.value)
async def exit_channel(request: web.Request) -> web.Response:
    return await ChannelController.exit_channel(request)


@channel_routes.get(Endpoints.GET_CHANNEL_ONLINE_USERS.value)
async def get_channel_online_users(request: web.Request) -> web.Response:
    return await ChannelController.get_channel_online_users(request)

@channel_routes.get(Endpoints.GET_ALL_CHANNELS.value)
async def get_all_channels(request: web.Request, *args,**kwargs) -> web.Response:
    return await ChannelController.get_all_channels(request)
    

@channel_routes.post(Endpoints.POST_CREATE_CHANNEL.value)
async def create_channel(request: web.Request) -> web.Response:
    return await ChannelController.create_channel(request)


@channel_routes.delete(Endpoints.DELETE_DELETE_CHANNEL.value)
async def delete_channel(request: web.Request) -> web.Response:
    return await ChannelController.delete_channel(request)

@channel_routes.put(Endpoints.PUT_UPDATE_CHANNEL_NAME.value)
async def update_channel_name(request: web.Request) -> web.Response:
    return await ChannelController.update_channel_name(request)


@channel_routes.put(Endpoints.PUT_UPDATE_PROMOTE_CHANNEL.value)
async def promote_channel(request: web.Request) -> web.Response:
    return await ChannelController.promote_channel(request)


@channel_routes.put(Endpoints.PUT_UPDATE_DEMOTE_CHANNEL.value)
async def demote_channel(request: web.Request) -> web.Response:
    return await ChannelController.demote_channel(request)


@channel_routes.delete(Endpoints.DELETE_ALL_MESSAGE.value)
async def delete_all_messages(request: web.Request) -> web.Response:
    return await ChannelController.delete_all_messages(request)


@channel_routes.delete(Endpoints.DELETE_CHANNEL_MESSAGES.value)
async def delete_channel_msgs(request: web.Request) -> web.Response:
    return await ChannelController.delete_channel_msgs(request)