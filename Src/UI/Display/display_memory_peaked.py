from .display_base import *

class DisplayMemoryPeaked(DisplayBase):
    def __init__(self, console):
        super().__init__(console)

    def load_img(self):
        self.display_image = self.console.reSize_Image(DISPLAY_PATH + "algo_display.png")

    def setup_pos(self):
        x, y = self.console.convertCoordinate(365, 670)
        a, b = self.console.convertCoordinate(270, 675)
        self.display = {
            "image": self.display_image,
            "pos": (self.console.screen_size // 2 - self.display_image.get_width() // 2 + x, y),
            "text_pos": (self.console.screen_size // 2 + a, b),
            "text": "MEMORY PEAKED : 0 MB"
        }

    def draw(self, screen):
        screen.blit(self.display["image"], self.display["pos"])
        if self.display["text"]:
            super().draw_text_on_display(screen, self.display["text"], self.display["text_pos"])

    def update_text(self, text):
        self.display["text"] = text