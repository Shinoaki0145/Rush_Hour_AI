from .popup_base import  *
import UI.Button.button_play as bplay
import UI.Button.button_pause as bpause
import UI.Button.button_exit as be
import UI.Button.button_back as bb

class PopupInfoInGame(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.play_button = bplay.ButtonPlay(console)
        self.pause_button = bpause.ButtonPause(console)
        self.exit_button = be.ButtonExit(console)
        self.back_button = bb.ButtonBack(console)

    def show(self):
        self.visible = True
        self.setup()

    def setup(self):
        self.play_button.button_image = self.console.reSize_Smaller_Image(BUTTON_PATH + "but_play.png")
        self.pause_button.button_image = self.console.reSize_Smaller_Image(BUTTON_PATH + "but_pause.png")
        self.exit_button.button_image = self.console.reSize_Smaller_Image(BUTTON_PATH + "but_exit.png")

        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2

        play_button_width = self.play_button.button_image.get_width()

        spacing_x = 100
        spacing_y = 20
        spacing_line = 70

        play_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y)
        pause_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y + spacing_line)
        exit_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y + 2 * spacing_line)
        back_pos = (popup_center_x - play_button_width + 170, popup_center_y - play_button_width + 130)

        self.play_button.button_pos = play_pos
        self.pause_button.button_pos = pause_pos
        self.exit_button.button_pos = exit_pos
        self.back_button.button_pos = back_pos

        self.play_button.update_img()
        self.pause_button.update_img()
        self.exit_button.update_img()
        self.back_button.update_img()
        
    def draw(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 135
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "INFO BUTTON IN GAME", 24, title_x, title_y)

        create_3d_text(screen, "Press play to choose Algorithm", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 80)
        create_3d_text(screen, "Press pause to pause game and", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 140)
        create_3d_text(screen, "press again to continue", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "Press exit to out game", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 220)

        self.play_button.draw(screen)
        self.pause_button.draw(screen)
        self.exit_button.draw(screen)
        self.back_button.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name == 'back_button'
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None
    