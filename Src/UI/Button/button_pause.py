from .button_base import *

class ButtonPause(ButtonBase):
    def __init__(self, console):
        super().__init__(console)
        self.name = "pause"

    def load_img(self):
        self.button_image = self.console.reSize_Image(BUTTON_PATH + "but_pause.png")

    def setup_pos(self):
        self.button_pos = (self.console.screen_size - self.button_image.get_width() - 310, 10)
    
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