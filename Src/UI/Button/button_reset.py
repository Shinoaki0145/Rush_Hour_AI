from .button_base import *

class ButtonReset(ButtonBase):
    def __init__(self, console):
        super().__init__(console)
        self.name = "reset"

    def load_img(self):
        self.button_image = self.console.reSize_Image(BUTTON_PATH + "but_reset.png")

    def setup_pos(self):
        x, y = self.console.convertCoordinate(250, 10)
        self.button_pos = (self.console.screen_size - self.button_image.get_width() - x, y)

    def update_img(self):
        self.button = {
            "image": self.button_image,
            "pos": self.button_pos,
            "rect": pygame.Rect(self.button_pos[0], 
                                self.button_pos[1], 
                                self.button_image.get_width(), 
                                self.button_image.get_height())
        } 
        
    def draw(self, screen):
        screen.blit(self.button["image"], self.button["pos"])
        