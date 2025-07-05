from UI.ui import *

class DisplayBase:
    def __init__(self, console):
        self.console = console
        self.displays = {}
        self.load_img()
        self.setup_pos()

    def load_img(self):
        raise NotImplementedError("Must be implemented.")

    def setup_pos(self):
        raise NotImplementedError("Must be implemented.")
    
    def draw_text_on_display(self, screen, text, pos):
        create_3d_text(screen, text, 20, pos[0], pos[1], self.console)