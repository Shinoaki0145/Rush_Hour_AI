import UI.Button.button_info as bi
import UI.Button.button_mute as bm
import UI.Button.button_pause as bpause
import UI.Button.button_reset as br
import UI.Button.button_play as bplay
import UI.Button.button_exit as be

class ButtonManager():
    def __init__(self, console):
        self.info = bi.ButtonInfo(console)
        self.mute = bm.ButtonMute(console)
        self.pause = bpause.ButtonPause(console)
        self.reset = br.ButtonReset(console)
        self.play = bplay.ButtonPlay(console)
        self.exit = be.ButtonExit(console)

    def draw_all(self, screen):
        self.info.draw(screen)
        self.mute.draw(screen)
        self.pause.draw(screen)
        self.reset.draw(screen)
        self.play.draw(screen)
        self.exit.draw(screen)