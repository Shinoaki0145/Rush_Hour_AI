from .popup_base import *

class PopupLose(PopupBase):
    def __init__(self, console):
        super().__init__(console)

        # Load button images cho lose popup
        self.buttons = {}
        self.lose_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png")
        }

    def show(self, level, algorithm="DFS"):
        self.level = level
        self.algorithm = algorithm
        self.setup()

    def setup(self):
        reset_button_image = self.lose_button_images["reset_level"]
        exit_button_image = self.lose_button_images["exit_level"]

        # Tính toán vị trí cho 2 buttons
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        reset_button_width = reset_button_image.get_width()
        exit_button_width = exit_button_image.get_width()
        
        reset_pos = (popup_center_x - reset_button_width - spacing_x//2, popup_center_y)
        exit_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["reset"] = {
            "image": reset_button_image,
            "pos": reset_pos,
            "rect": pygame.Rect(reset_pos[0], reset_pos[1], reset_button_width, reset_button_image.get_height()),
        }

        self.buttons["exit"] = {
            "image": exit_button_image,
            "pos": exit_pos,
            "rect": pygame.Rect(exit_pos[0], exit_pos[1], exit_button_width, exit_button_image.get_height()),
        }

    def draw(self, screen):
        """Vẽ lose message popup"""
        congrat_text = f"YOU LOST!"
        info_text = f"YOU FAILED LEVEL {self.level}"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 20
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        # Info text
        info_x = popup_center_x - len(info_text) * 4 - 20
        info_y = self.popup_pos[1] + 100
        create_3d_text(screen, info_text, 16, info_x, info_y)
        
        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 130
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