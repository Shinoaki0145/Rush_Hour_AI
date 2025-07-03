from .display_base import *

class DisplayMoves(DisplayBase):
    def __init__(self, console):
        super().__init__(console)

    def load_img(self):
        self.display_image = self.console.reSize_Image(DISPLAY_PATH + "moves_display.png")

    def setup_pos(self):
        self.display = {
                "image": self.display_image,
                "pos": (self.console.screen_size - 300, 175),
                "text_pos": (self.console.screen_size - 286, 179),
                "text": "MOVES :  0"
            }

    def draw(self, screen):
        screen.blit(self.display["image"], self.display["pos"])
        if self.display["text"]:
            super().draw_text_on_display(screen, self.display["text"], self.display["text_pos"])

    def update_text(self, text):
        self.display["text"] = text
