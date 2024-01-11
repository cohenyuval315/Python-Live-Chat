from view.channel_window import ChannelWindow
from exceptions import ErrorMessage
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
    
    @staticmethod
    def catch_error_message(func):
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except ErrorMessage as e:
                self.channel_window.add_line(f'{e}', 'gray')

        return wrapper