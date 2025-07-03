from UI.ui import *

class PopupBase:
    def __init__(self, console):
        self.console = console
        self.visible = False
        self.setup_popup()
    
    def setup_popup(self):
        """Setup popup background"""
        self.popup_bg = self.console.reSize_Image(DISPLAY_PATH + "msg_display.png")
        
        # Tính toán vị trí giữa màn hình
        self.popup_pos = (
            (self.console.screen_size - self.popup_bg.get_width()) // 2,
            (self.console.screen_size - self.popup_bg.get_height()) // 2
        )