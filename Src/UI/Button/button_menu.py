import UI.Button.button_info as bi
import UI.Button.button_mute as bm
import UI.Button.button_sound as bs
import UI.Button.button_play as bp
import UI.Button.button_exit as be
from UI.ui import *

class ButtonMenu:
    def __init__(self, console):
        self.console = console
        self.info = bi.ButtonInfo(console)
        self.mute = bm.ButtonMute(console)
        self.sound = bs.ButtonSound(console)
        self.play = bp.ButtonPlay(console)
        self.exit = be.ButtonExit(console)
        self.load_button_images()
        self.setup_button_positions()

        self.is_muted = False

    def load_button_images(self):
        self.info.button_image = self.console.reSize_Bigger_Image(BUTTON_PATH + "but_info.png")
        self.mute.button_image = self.console.reSize_Bigger_Image(BUTTON_PATH + "but_mute.png")
        self.sound.button_image = self.console.reSize_Bigger_Image(BUTTON_PATH + "but_sound.png")
        self.play.button_image = self.console.reSize_Bigger_Image(BUTTON_PATH + "but_play.png")
        self.exit.button_image = self.console.reSize_Bigger_Image(BUTTON_PATH + "but_exit.png")

    def setup_button_positions(self):
        button_height = self.console.screen_size // 3 * 2 - self.play.button_image.get_height() // 2
        self.info.button_pos = self.console.screen_size // 5 * 2 - self.info.button_image.get_width() // 2, button_height
        self.mute.button_pos = self.console.screen_size // 5 * 3 - self.mute.button_image.get_width() // 2, button_height
        self.sound.button_pos = self.console.screen_size // 5 * 3 - self.sound.button_image.get_width() // 2, button_height
        self.play.button_pos = self.console.screen_size // 5 - self.play.button_image.get_width() // 2, button_height
        self.exit.button_pos = self.console.screen_size // 5 * 4 - self.exit.button_image.get_width() // 2, button_height

        self.info.update_img()
        self.mute.update_img()
        self.sound.update_img()
        self.play.update_img()
        self.exit.update_img()

    def draw_all(self, screen):
        self.info.draw(screen)
        if self.is_muted:
            self.mute.draw(screen)
        else:
            self.sound.draw(screen)
        self.play.draw(screen)
        self.exit.draw(screen)