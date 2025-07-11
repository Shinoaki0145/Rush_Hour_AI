from .button_base import *

class ButtonBack(ButtonBase):
    def __init__(self, console):
        super().__init__(console)
        self.name = "back"

    def load_img(self):
        self.button_image = self.console.reSize_Smaller_Image(BUTTON_PATH + "but_back.png")

    def setup_pos(self):
        self.button_pos = self.console.convertCoordinate(215, 160)
        
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