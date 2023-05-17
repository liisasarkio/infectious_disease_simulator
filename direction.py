class Direction:
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

    def __init__(self):
        self.all_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    def get_all_directions(self):
        return self.all_directions

    @staticmethod
    def get_x_step(self, dir):
        return dir[0]
    @staticmethod
    def get_y_step(self, dir):
        return dir[1]