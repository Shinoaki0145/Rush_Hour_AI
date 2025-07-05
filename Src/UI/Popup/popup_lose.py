from .popup_base import *
import UI.Button.button_reset as br
import UI.Button.button_exit as be

class PopupLose(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.reset = br.ButtonReset(console)
        self.exit = be.ButtonExit(console)

    def show(self, level, algorithm="DFS"):
        self.level = level
        self.algorithm = algorithm
        self.visible = True
        self.setup()

    def setup(self):
        x, y = self.console.convertCoordinate(130, 50)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + y
        
        spacing_x = x
        
        reset_pos = (popup_center_x - self.reset.button_image.get_width() - spacing_x // 2, popup_center_y)
        exit_pos = (popup_center_x + spacing_x // 2, popup_center_y)
        
        self.reset.button_pos = reset_pos
        self.exit.button_pos = exit_pos

        self.reset.update_img()
        self.exit.update_img()

    def draw(self, screen):
        congrat_text = f"YOU LOST !"
        info_text = f"YOU FAILED LEVEL {self.level}"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2

        x, y = self.console.convertCoordinate(90, 20)
        title_x = popup_center_x - x
        title_y = self.popup_pos[1] + y
        create_3d_text(screen, congrat_text, 40, title_x, title_y, self.console)

        x, y = self.console.convertCoordinate(len(info_text) * 5 + 20, 80)
        info_x = popup_center_x - x
        info_y = self.popup_pos[1] + y
        create_3d_text(screen, info_text, 30, info_x, info_y, self.console)

        x, y = self.console.convertCoordinate(len(algorithm_text) * 5 + 30, 120)
        algorithm_x = popup_center_x - x
        algorithm_y = self.popup_pos[1] + y
        create_3d_text(screen, algorithm_text, 30, algorithm_x, algorithm_y, self.console)
        
        self.reset.draw(screen)
        self.exit.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name in ['reset', 'exit'] 
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None