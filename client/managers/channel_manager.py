from view.channel_window import ChannelWindow
from .manager_base import ManagerBase
from apis.channel_api import ChannelAPI
from utils import is_valid_status
class ChannelManager(ManagerBase):

    def __init__(self, channel_window: ChannelWindow,channel_api:ChannelAPI) -> None:
        super().__init__(channel_window)
        self.channel_api = channel_api
        self.channels = []
        self.colors = []

    def get_api(self) -> ChannelAPI:
        return self.channel_api
    @ManagerBase.catch_error_message
    async def update(self,token):
        res = await self.channel_api.get_all_channels(token)   
        if not is_valid_status(res):
            return res
        res = res['data']
        await self._set_channels(res)
        await self._print_view()


    async def _set_channels(self,online_channels:list[dict]=[],clear=True):
        if clear:
            await self._clear_channels()
        self.channels = online_channels

    async def _print_view(self,clear=True):
        if clear:
            await self._clear_view()
        for channel in self.channels:
            name = channel['name']
            color = channel['color']
            self.channel_window.add_channel(name,color)
    
    async def _clear_view(self):
        self.channel_window.clear_channels()

    async def _clear_channels(self):
        self.channels.clear()
    
