from .popup_base import  *
import UI.Button.button_reset as br
import UI.Button.button_next as bn

class PopupWin(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.reset = br.ButtonReset(console)
        self.next_level = bn.ButtonNext(console)

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
        
        reset_pos = (popup_center_x - self.reset.button_image.get_width() - spacing_x // 2, popup_center_y)
        next_pos = (popup_center_x + spacing_x // 2, popup_center_y)
        
        self.reset.button_pos = reset_pos
        self.next_level.button_pos = next_pos

        self.reset.update_img()
        self.next_level.update_img()
        
    def draw(self, screen):
        congrat_text = f"CONGRATULATIONS!"
        info_text_1 = f"YOU WIN LEVEL {self.level}"
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
        
        self.reset.draw(screen)
        self.next_level.draw(screen)
    
    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name in ['reset', 'next_level'] 
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None
