from .popup_base import  *

class PopupWin(PopupBase):
    def __init__(self, console):
        super().__init__(console)

        # Win popup specific data
        self.level = 0
        self.moves = 0
        self.cost = 0
        self.algorithm = ""

        # Load button images cho win popup
        self.buttons = {}
        self.win_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "next_level": self.console.reSize_Image(BUTTON_PATH + "but_play.png")
        }

    def show(self, level, moves, cost, algorithm="DFS"):
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.setup()

    def setup(self):
        reset_button_image = self.win_button_images["reset_level"]
        next_button_image = self.win_button_images["next_level"]
        
        # Tính toán vị trí cho 2 buttons
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        reset_button_width = reset_button_image.get_width()
        next_button_width = next_button_image.get_width()
        
        reset_pos = (popup_center_x - reset_button_width - spacing_x//2, popup_center_y)
        next_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["reset"] = {
            "image": reset_button_image,
            "pos": reset_pos,
            "rect": pygame.Rect(reset_pos[0], reset_pos[1], reset_button_width, reset_button_image.get_height()),
        }
        
        self.buttons["next_level"] = {
            "image": next_button_image,
            "pos": next_pos,
            "rect": pygame.Rect(next_pos[0], next_pos[1], next_button_width, next_button_image.get_height()),
        }
        
    def draw(self, screen):
        """Vẽ win message popup"""
        congrat_text = f"CONGRATULATIONS!"
        info_text_1 = f"YOU WIN LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        # Info text
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        # Vẽ buttons - sử dụng button images có sẵn
        for _, button_data in self.buttons.items():
            # Vẽ button image
            screen.blit(button_data["image"], button_data["pos"])

    def check_button_click(self, mouse_pos):
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None