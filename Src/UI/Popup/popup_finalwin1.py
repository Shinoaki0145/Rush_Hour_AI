from .popup_base import *

class PopupFinalWin1(PopupBase):
    def __init__(self, console):
        super().__init__(console)

        self.buttons = {}
        self.level = 0
        self.moves = 0
        self.cost = 0
        self.algorithm = ""

        self.final_win_1_button_images = {
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png"),
            "next_popup": self.console.reSize_Image(BUTTON_PATH + "but_play.png")  # Dùng play button cho "next"
        }

    def show(self, level, moves, cost, algorithm="DFS"):
        """Hiển thị final win popup đầu tiên (giống win popup nhưng có exit và next)"""
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.setup()

    def setup(self):
        """Setup buttons cho final_win_1 popup"""
        exit_button_image = self.final_win_1_button_images["exit_level"]
        next_button_image = self.final_win_1_button_images["next_popup"]
        
        # Tính toán vị trí cho 2 buttons (giống như win popup)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        exit_button_width = exit_button_image.get_width()
        next_button_width = next_button_image.get_width()
        
        exit_pos = (popup_center_x - exit_button_width - spacing_x//2, popup_center_y)
        next_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["exit"] = {
            "image": exit_button_image,
            "pos": exit_pos,
            "rect": pygame.Rect(exit_pos[0], exit_pos[1], exit_button_width, exit_button_image.get_height()),
        }
        
        self.buttons["next_popup"] = {
            "image": next_button_image,
            "pos": next_pos,
            "rect": pygame.Rect(next_pos[0], next_pos[1], next_button_width, next_button_image.get_height()),
        }

    def draw(self, screen):
        """Vẽ final win 1 popup (giống win popup)"""
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
        create_3d_text(screen, info_text_2, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        # Vẽ buttons
        for _, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])

    def check_button_click(self, mouse_pos):
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None