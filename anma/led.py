class Led:
    def __init__(self, rgb):
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

    def on(self, rgb):
        print(rgb)
        r, g, b = rgb
        self.r.start(r)
        self.g.start(g)
        self.b.start(b)

    def off(self):
        pass
