from .popup_base import *

class PopupAlgo(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        
        self.buttons = {}
        
    def show(self):
        self.setup()
        
    def setup(self):

        button_image = self.console.reSize_Image(BUTTON_PATH + "but_start.png")
        
        algorithms = ["BFS", "DFS", "A STAR", "UCS"]
        button_width = button_image.get_width()
        button_height = button_image.get_height()
        
        # Tính toán vị trí buttons (2x2 grid)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        
        spacing_x = 20
        spacing_y = 20
        
        positions = [
            (popup_center_x - button_width - spacing_x//2, popup_center_y - button_height - spacing_y//2),  # BFS
            (popup_center_x + spacing_x//2, popup_center_y - button_height - spacing_y//2),  # DFS
            (popup_center_x - button_width - spacing_x//2, popup_center_y + spacing_y//2),  # A STAR
            (popup_center_x + spacing_x//2, popup_center_y + spacing_y//2)   # UCS
        ]
        
        for i, algorithm in enumerate(algorithms):
            self.buttons[algorithm] = {
                "image": button_image,
                "pos": positions[i],
                "rect": pygame.Rect(positions[i][0], positions[i][1], button_width, button_height),
                "text": algorithm
            }
            
    def draw(self, screen):
        """Vẽ algorithm selection popup"""
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 120
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, "CHOOSE ALGORITHM", 24, title_x, title_y)
        
        for algorithm, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
            
            text_x = button_data["pos"][0] + button_data["image"].get_width() // 2 - len(algorithm) * 6
            text_y = button_data["pos"][1] + button_data["image"].get_height() // 2 - 10
            create_3d_text(screen, algorithm, 16, text_x, text_y)

    def check_button_click(self, mouse_pos):
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None