from .popup_base import *
import UI.Button.button_exit as be
import UI.Button.button_next as bn

class PopupFinalWin(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.exit = be.ButtonExit(console)
        self.next_popup = bn.ButtonNext(console)

        self.level = 0
        self.moves = 0
        self.cost = 0
        self.algorithm = ""

    def show(self, level, moves, cost, algorithm="DFS"):
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.visible = True
        self.setup()

    def setup(self):
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        exit_pos = (popup_center_x - self.exit.button_image.get_width() - spacing_x //2 , popup_center_y)
        next_pos = (popup_center_x + spacing_x // 2, popup_center_y)
        
        self.exit.button_pos = exit_pos
        self.next_popup.button_pos = next_pos

        self.exit.update_img()
        self.next_popup.update_img()

    def draw(self, screen):
        congrat_text = f"FANTASTIC BABY!"
        info_text_1 = f"YOU WIN FINAL LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        self.exit.draw(screen)
        self.next_popup.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name in ['exit', 'next_popup'] 
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None