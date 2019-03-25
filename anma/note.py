import handle


class Note:
    def __init__(self, name, pitch, color):
        self.name = name
        self.pitch = pitch
        self.color = color
        self.on = False

    def play(self, hndl, velocity=127):
        if not self.on:
            if hndl.arg.verbose:
                print(f"name: {self.name} pitch: {self.pitch} "
                      f"color: {self.color}")
            hndl.player.note_on(self.pitch, velocity)
            self.on = True

    def stop(self, hndl):
        if self.on:
            hndl.player.note_off(self.pitch)
            self.on = False
