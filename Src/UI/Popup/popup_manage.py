import UI.Popup.popup_algo as pa
import UI.Popup.popup_win as pw
import UI.Popup.popup_lose  as pl
import UI.Popup.popup_finalwin1 as pf1
import UI.Popup.popup_finalwin2 as pf2
from UI.ui import *

class GamePopup:
    def __init__(self, console):
        self.algo = pa.PopupAlgo(console)
        self.win = pw.PopupWin(console)
        self.lose = pl.PopupLose(console)
        self.finalwin1 = pf1.PopupFinalWin1(console)
        self.finalwin2 = pf2.PopupFinalWin2(console)

        self.console = console
        self.visible = False
        self.popup_type = None  # "algorithm", "win", "lose", or "final_win"

    def update(self, visible, popup_type):
        self.visible = visible
        self.popup_type = popup_type
        
    def hide(self):
        """Ẩn popup"""
        self.visible = False
        self.popup_type = None

    def draw(self, screen):
        """Vẽ popup và buttons"""
        if not self.visible:
            return
        
        # Vẽ popup background
        screen.blit(self.algo.popup_bg, self.algo.popup_pos)
        
        if self.popup_type == "algorithm":
            self.algo.draw(screen)
        elif self.popup_type == "win":
            self.win.draw(screen)
        elif self.popup_type == "lose":
            self.lose.draw(screen)
        elif self.popup_type == "final_win_1":
            self.finalwin1.draw(screen)
        elif self.popup_type == "final_win_2":
            self.finalwin2.draw(screen)

    def check_button_click(self, mouse_pos):
        """Kiểm tra click vào buttons"""
        if not self.visible:
            return None
        
        if (self.algo.check_button_click(mouse_pos) or
            self.win.check_button_click(mouse_pos) or
            self.lose.check_button_click(mouse_pos) or
            self.finalwin1.check_button_click(mouse_pos) or
            self.finalwin2.check_button_click(mouse_pos)):
                # KHÔNG tự động ẩn popup ở đây
                # Để game_manage.py xử lý việc ẩn popup
            return "clicked"
        
        return None
    