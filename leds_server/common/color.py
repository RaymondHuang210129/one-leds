class Color:
    def __init__(self, red=0, green=0, blue=0):
        for brightness in [red, green, blue]:
            if brightness < 0 or brightness > 255:
                raise RuntimeError("The brightness value must within [0:255]")
        self.red: int = red
        self.green: int = green
        self.blue: int = blue
