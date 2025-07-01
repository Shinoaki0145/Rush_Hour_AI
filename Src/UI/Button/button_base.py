from UI.ui import *

class ButtonBase():
    def __init__(self, console):
        self.console = console
        self.button = {}
        self.load_img()
        self.setup_pos()
        self.update_img()

    def load_img(self):
        raise NotImplementedError("Must be implemented.")

    def setup_pos(self):
        raise NotImplementedError("Must be implemented.")
    
    def update_img(self):
        raise NotImplementedError("Must be implemented.")