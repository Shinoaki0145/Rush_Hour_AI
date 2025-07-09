from .popup_base import *
import UI.Button.button_exit as be
import UI.Button.button_next as bn

class PopupFinalLose(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.next_level = bn.ButtonNext(console)
        self.exit = be.ButtonExit(console)

    def show(self, level):
        self.level = level
        self.visible = True
        self.setup()

    def setup(self):
        x, y = self.console.convertCoordinate(130, 50)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + y
        
        spacing_x = x
        
        exit_pos = (popup_center_x - self.next_level.button_image.get_width() - spacing_x // 2, popup_center_y)
        next_pos = (popup_center_x + spacing_x // 2, popup_center_y)
        
        self.next_level.button_pos = next_pos
        self.exit.button_pos = exit_pos

        self.next_level.update_img()
        self.exit.update_img()

    def draw(self, screen):
        congrat_text = f"MAP IS UNSOLVABLE"
        info_text = f"MAP HAS BEEN BLOCKED"
        win_text = f"YOU WIN LEVEL {self.level}"

        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2

        x, y = self.console.convertCoordinate(150, 80)
        create_3d_text(screen, congrat_text, 40, popup_center_x - x, self.popup_pos[1] + y, self.console)

        x, y = self.console.convertCoordinate(135, 120)
        create_3d_text(screen, info_text, 30, popup_center_x - x, self.popup_pos[1] + y, self.console)

        x, y = self.console.convertCoordinate(len(win_text) * 5 + 58, 20)
        info_x = popup_center_x - x
        info_y = self.popup_pos[1] + y
        create_3d_text(screen, win_text, 40, info_x, info_y, self.console)

        self.next_level.draw(screen)
        self.exit.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name in ['exit', 'next_level'] 
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None