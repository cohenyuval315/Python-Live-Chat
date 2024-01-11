import asyncio
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.data_structures import Point
from prompt_toolkit import layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit import widgets
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.scroll import scroll_half_page_up,scroll_half_page_down,scroll_one_line_up,scroll_one_line_down
from prompt_toolkit.formatted_text import to_formatted_text,to_plain_text
import time

def normalized_line(max_width:int,line:str):
    #line_len = len(line.replace(' ', ''))
    line_len = len(line)
    if line_len < max_width:
        return line
    normalized_line = ""
    while line_len > max_width:
        normalized_line += line[:max_width] + '\n'
        line = line[max_width:]
    normalized_line = normalized_line[:len(normalized_line) - 1]
    return normalized_line

class ChannelWindow:
    CHAT_WIDTH = 75
    PAGE_SIZE = 5
    MAX_CHAT_MESSAGE = CHAT_WIDTH * 3
    def __init__(self, add_input_lines_to_text=False,onExit=None):
        self._last_y = -1
        self.onExit = onExit
        self._input_buffer = Buffer(multiline=False, accept_handler=self._input_handler)
        self._identity_control = FormattedTextControl()  
        self._header_control = FormattedTextControl() 
        self._users_control = FormattedTextControl()
        self._channels_control = FormattedTextControl()
        self._text_control = FormattedTextControl(get_cursor_position=self._get_cursor_position) 
        self._identity_control_window = Window(content=self._identity_control,height=1)
        self._text_control_window = Window(content=self._text_control,width=self.CHAT_WIDTH)
        self._header_control_window= Window(content=self._header_control, height=1)
        self._root_container = self._make_layout()
        self._input_queue = asyncio.Queue()
        self._add_input_lines_to_text = add_input_lines_to_text
        self._app = None
        self._key_bindings = self._get_key_bindings()

        self._style = Style.from_dict({
            "system": "ansiyellow",
            "guest" : "",
            "user" : "ansiblue",
            "moderator" : "ansigreen",
            "admin" : "ansired",

            "all_channel" : "",
            "user_channel" : "ansiblue",
            "moderator_channel": "ansigreen",
            "admin_channel": "ansired",

            "_msg":"",
            "user_msg":"ansiblue",
            "moderator_msg": "ansigreen",
            "admin_msg": "ansired"
            
        })

    
    def _get_key_bindings(self):
        kb = KeyBindings()
        kb.add("c-space")(focus_next)
        @kb.add('pageup')
        def _(event):
            self._last_y -= self.PAGE_SIZE
            def move_up_cursor_pos():
                return Point(0,max(0,self._last_y))
            self._text_control.get_cursor_position = move_up_cursor_pos

        @kb.add('pagedown')
        def _(event):
            self._last_y += self.PAGE_SIZE
            if self._last_y > str(to_plain_text(self._text_control.text)).count("\n"):
                self._text_control.get_cursor_position = self._get_cursor_position
                return
            def move_down_cursor_pos():
                return Point(0,min(self._last_y,str(to_plain_text(self._text_control.text)).count("\n")))
            self._text_control.get_cursor_position = move_down_cursor_pos

        @kb.add('tab')
        def _(event):
            self._text_control.get_cursor_position = self._get_cursor_position
            
        @kb.add('f4')
        async def _(event):
            await self.exit()
        return kb

    async def run(self):
        self._app = Application(layout=Layout(self._root_container), full_screen=True, refresh_interval=0.1,style=self._style,mouse_support=True,key_bindings=self._key_bindings)
        try:
            await self._app.run_async()
        except asyncio.CancelledError:
            self.exit()
            raise

    async def exit(self):
        self.add_line('---- exiting... ----','gray')
        await asyncio.sleep(1)        
        if self._app and self._app.is_running:
            self._app.exit()

    def add_line(self, line: str,style_class=""):
        """Add a line to upper window"""
        self._add_line_to_control(line, self._text_control,style_class)
        self._text_control.get_cursor_position = self._get_cursor_position
        

        
    
    def clear_identity(self):
        self.clear(self._identity_control)

    def change_identity(self,line:str):
        self.clear_identity()
        identity  = "user: " + line
        self._add_line_to_control(identity,self._identity_control)

    def change_header(self,line:str):
        self.clear_header()
        header = "#" * 10 + " " + line + " " + "#" * 10
        self._add_line_to_control(header,self._header_control)

    def clear_header(self):
        self.clear(self._header_control)

    def add_user(self, nickname: str,style_class=""):
        self._add_line_to_control(nickname, self._users_control,style_class)

    def clear_users(self):
        self.clear(self._users_control)

    def add_channel(self, channel: str,style_class=""):
        self._add_line_to_control(channel, self._channels_control,style_class)

    def clear_channels(self):
        self.clear(self._channels_control)


    def clear_messages(self):
        self.clear(self._text_control)

    def clear(self, control):
        control.text = ""

    async def get_next_input_line(self):
        """Gets the next sent input line from the user"""
        return await self._input_queue.get()

        
    @classmethod
    def _add_line_to_control(cls, line, control, style_class=""):
        #line = normalized_line(cls.CHAT_WIDTH,line)
        #control.cursor_position = Point(0, str(to_plain_text(control.text)).count("\n"))
        if control.text:
            #control.text = to_formatted_text([styled_line])
            control.text.append((style_class,"\n" + line))
            #control.text = "\n".join([text,line])
            #control.text = to_formatted_text([t for t in control.text])
        else:
            control.text = to_formatted_text([(style_class,line)])
        

    def _make_layout(self):
        return layout.VSplit([
            layout.HSplit([
                self._header_control_window,
                widgets.HorizontalLine(),
                self._text_control_window,
                widgets.HorizontalLine(),
                Window(content=BufferControl(buffer=self._input_buffer), height=1,
                       width=layout.Dimension(weight=10)),
            ]),
            widgets.VerticalLine(),
            layout.HSplit([
                layout.VSplit([
                    Window(content=self._users_control, width=layout.Dimension(weight=1, max=20)),
                    widgets.VerticalLine(),
                    Window(content=self._channels_control, width=layout.Dimension(weight=1, max=20)),                
                ]),
                widgets.HorizontalLine(),
                self._identity_control_window,         
            ])


        ])

    def _input_handler(self, buffer):
        if self._add_input_lines_to_text:
            self.add_line(buffer.text)
        self._input_queue.put_nowait(buffer.text)
        return False
    

    def _get_cursor_position(self):
        last_y = str(to_plain_text(self._text_control.text)).count("\n")
        self._last_y = last_y
        return Point(0, self._last_y) # type: ignore


def main():
    asyncio.run(ChannelWindow(add_input_lines_to_text=True).run())


if __name__ == "__main__":
    main()
