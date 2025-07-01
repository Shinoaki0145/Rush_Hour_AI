from .display_base import *

class DisplayCost(DisplayBase):
    def __init__(self, console):
        super().__init__(console)

    def load_img(self):
        self.display_image = self.console.reSize_Image(DISPLAY_PATH + "level_display.png")

    def setup_pos(self):
        self.display = {
                "image": self.display_image,
                "pos": (self.console.screen_size - 190, 175),
                "text_pos": (self.console.screen_size - 173, 179),
                "text": "COSTS :  0"
            }

    def draw(self, screen):
        # Vẽ hình ảnh display
        screen.blit(self.display["image"], self.display["pos"])
        # Vẽ text lên display
        if self.display["text"]:
            super().draw_text_on_display(screen, self.display["text"], self.display["text_pos"])

    def update_text(self, text):
        self.display["text"] = text
        print(f"DisplayManager: Updated costs to: {text}")  # Debug line 