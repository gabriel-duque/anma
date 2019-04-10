import handle


class Note:
    def __init__(self, name, pitch, led):
        self.name = name
        self.pitch = pitch
        self.on = False
        self.led = led

    def play(self, hndl, velocity=127, color=[100, 0, 100]):
        if not self.on:
            if hndl.arg.verbose:
                print("name: {} pitch: {} ".format(self.name, self.pitch) + "color: {}".format(self.color))
            hndl.player.note_on(self.pitch, velocity)
            self.led.on(color)
            self.on = True

    def stop(self, hndl):
        if self.on:
            hndl.player.note_off(self.pitch)
            self.on = False
