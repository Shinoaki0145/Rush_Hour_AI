import UI.Button.button_info as bi
import UI.Button.button_mute as bm
import UI.Button.button_sound as bs
import UI.Button.button_pause as bpause
import UI.Button.button_next as bn
import UI.Button.button_reset as br
import UI.Button.button_play as bplay
import UI.Button.button_exit as be

class ButtonManager:
    def __init__(self, console):
        self.info = bi.ButtonInfo(console)
        self.mute = bm.ButtonMute(console)
        self.sound = bs.ButtonSound(console)
        self.pause = bpause.ButtonPause(console)
        self.next = bn.ButtonNext(console)
        self.reset = br.ButtonReset(console)
        self.play = bplay.ButtonPlay(console)
        self.exit = be.ButtonExit(console)

        self.is_muted = False
        self.is_paused = False

    def draw_all(self, screen):
        self.info.draw(screen)
        if self.is_muted:
            self.mute.draw(screen)
        else:
            self.sound.draw(screen)
        if not self.is_paused:
            self.pause.draw(screen)
        else:
            self.next.draw(screen)
        self.reset.draw(screen)
        self.play.draw(screen)
        self.exit.draw(screen)