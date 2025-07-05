from .popup_base import *

class PopupChooseLv(PopupBase):
    def __init__(self, console):
        super().__init__(console)

        self.buttons = {}
        self.choose_lv_button_images = {
            "level_button": self.console.reSize_Image(BUTTON_PATH + "level_unlock.png"),
        }

    def show(self):
        self.visible = True
        self.setup()

    def setup(self):
        level_button_image = self.choose_lv_button_images["level_button"]
        button_width = level_button_image.get_width()
        button_height = level_button_image.get_height()

        # (3 rows × 4 columns)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        spacing_x, spacing_y = self.console.convertCoordinate(20, 20)

        # grid 3×4
        total_width = 4 * button_width + 3 * spacing_x
        total_height = 3 * button_height + 2 * spacing_y
        
        start_x = popup_center_x - total_width // 2
        start_y = popup_center_y - total_height // 2

        for i in range(12):
            row = i // 4  
            col = i % 4  
            
            level_pos = (
                start_x + col * (button_width + spacing_x),
                start_y + row * (button_height + spacing_y)
            )
            
            level_name = str(i + 1)
            self.buttons[f"level_{level_name}"] = {
                "image": level_button_image,
                "pos": level_pos,
                "rect": pygame.Rect(level_pos[0], level_pos[1], button_width, button_height),
                "text": level_name
            }

    def draw(self, screen):
        win_text = "Select a level to start playing"
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        x, y = self.console.convertCoordinate(212, 20)
        win_text_x = popup_center_x - x
        win_text_y = self.popup_pos[1] + y
        create_3d_text(screen, win_text, 40, win_text_x, win_text_y, self.console)
        i = self.console.convertCoordinate(0, 20)[1]

        for _, button_data in self.buttons.items():
            adjusted_pos = (button_data["pos"][0], button_data["pos"][1] + i)
            screen.blit(button_data["image"], adjusted_pos)
            level_text = button_data["text"]
            a, b = self.console.convertCoordinate(len(level_text) * 7, 25)
            text_x = adjusted_pos[0] + button_data["image"].get_width() // 2 - a
            text_y = adjusted_pos[1] + button_data["image"].get_height() // 2 - b
            create_3d_text(screen, level_text, 40, text_x, text_y, self.console)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):   
                return button_name
        return None
