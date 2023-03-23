from brain import Brain
class Spreader(Brain):
    def __init__(self):
        super.__init__()
        self.spreaded = 0 # how many cases has this spreader caused

    def touch_spread(self, other):
        if other in self.square.robots:
            # spread
        self.spreaded += 1

    def air_spread(self, other):
        self.spreaded += 1


