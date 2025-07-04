import UI.Popup.popup_algo as pa
import UI.Popup.popup_win as pw
import UI.Popup.popup_lose  as pl
import UI.Popup.popup_final_win as pfw
import UI.Popup.popup_choose_lv as pcl
import UI.Popup.popup_info_menu as pim
import UI.Popup.popup_info_ingame as piig
from UI.ui import *

class GamePopup:
    def __init__(self, console):
        self.algo = pa.PopupAlgo(console)
        self.win = pw.PopupWin(console)
        self.lose = pl.PopupLose(console)
        self.final_win = pfw.PopupFinalWin(console)
        self.choose_lv = pcl.PopupChooseLv(console)
        self.info_menu = pim.PopupInfoMenu(console)
        self.info_ingame = piig.PopupInfoInGame(console)

        self.popup_names = ['algo', 'win', 'lose', 'final_win', 'choose_lv', 'info_menu', 'info_ingame']
        
        self.console = console
        self.visible = False
        self.popup_type = None
        
    def hide(self):
        for popup_name, popup in self.__dict__.items():
            if popup_name in self.popup_names:
                popup.visible = False

        self.visible = False
        self.popup_type = None

    def update_type(self, popup_type):
        self.popup_type = popup_type
        self.visible = True

    def draw(self, screen):
        if not self.popup_type:
            return
        
        screen.blit(self.algo.popup_bg, self.algo.popup_pos)

        if self.popup_type == "algorithm":
            self.algo.draw(screen)
        elif self.popup_type == "win":
            self.win.draw(screen)
        elif self.popup_type == "lose":
            self.lose.draw(screen)
        elif self.popup_type == "final_win":
            self.final_win.draw(screen)
        elif self.popup_type == "choose_level":
            self.choose_lv.draw(screen)
        elif self.popup_type == "info_menu":
            self.info_menu.draw(screen)
        elif self.popup_type == "info_buttons":
            self.info_ingame.draw(screen)

    def check_button_click(self, mouse_pos):
        for popup_name, popup in self.__dict__.items():
            if popup_name in self.popup_names:
                button_name = popup.check_button_click(mouse_pos)
                if button_name:
                    return button_name
        return None
    