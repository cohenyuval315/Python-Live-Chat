from .channel_window import ChannelWindow
class ManagerBase():
    def __init__(self,channel_window:ChannelWindow) -> None:
        self.channel_window = channel_window

    async def handle_response(self,res):
        if isinstance(res,str):
            pass
        if isinstance(res,list):
            pass
        if isinstance(res,dict):
            pass
        return res