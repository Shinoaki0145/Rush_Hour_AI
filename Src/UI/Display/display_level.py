from .display_base import *

class DisplayLevel(DisplayBase):
    def __init__(self, console):
        super().__init__(console)

    def load_img(self):
        self.display_image = self.console.reSize_Image(DISPLAY_PATH + "level_display.png")

    def setup_pos(self):
        self.display = {
                "image": self.display_image, 
                "pos": (205, 175),
                "text_pos": (222, 179),
                "text": "LEVEL :  0"
            }

    def draw(self, screen):
        # Vẽ hình ảnh display
        screen.blit(self.display["image"], self.display["pos"])
        # Vẽ text lên display
        if self.display["text"]:
            super().draw_text_on_display(screen, self.display["text"], self.display["text_pos"])

    def update_text(self, text):
        self.display["text"] = text
        print(f"DisplayManager: Updated level to: {text}")  # Debug line 