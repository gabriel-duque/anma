import handle
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class Note:
    def __init__(self, name, pitch, led, coord):
        self.name = name
        self.pitch = pitch
        self.on = False
        self.led = led
        self.coord = coord

    def __repr__(self):
        return self.name

    def play(self, hndl, velocity=127, color=[100, 0, 100]):
        if not self.on:
            if hndl.arg.verbose:
                print("name: {} pitch: {} ".format(self.name, self.pitch) + "color: {}".format(self.color))
            hndl.player.note_on(self.pitch, velocity)
            self.led.on(color)
            self.update_screen(hndl, color)
            self.on = True

    def stop(self, hndl):
        if self.on:
            hndl.player.note_off(self.pitch)
            self.on = False

    def update_screen(self, hndl, color):
        pygame.draw.rect(hndl.screen, color, self.coord)
        pygame.display.update()
