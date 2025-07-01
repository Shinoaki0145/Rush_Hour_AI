from .display_base import *

class DisplayAlgo(DisplayBase):
    def __init__(self, console):
        super().__init__(console)

    def load_img(self):
        self.display_image = self.console.reSize_Image(DISPLAY_PATH + "algo_display.png")

    def setup_pos(self):
        self.display = {
            "image": self.display_image,
            "pos": (self.console.screen_size // 2 - 85, 175),
            "text_pos": (self.console.screen_size // 2 - 55, 179),
            "text": "ALGORITHM :  "
        }

    def draw(self, screen):
        # Vẽ hình ảnh display
        screen.blit(self.display["image"], self.display["pos"])
        # Vẽ text lên display
        if self.display["text"]:
            super().draw_text_on_display(screen, self.display["text"], self.display["text_pos"])

    def update_text(self, text):
        self.display["text"] = text
        print(f"DisplayManager: Updated algorithm to: {text}")  # Debug line 