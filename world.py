from spreader import Spreader
import random
from square import Square
from coordinates import Coordinates
from susceptible import Susceptible


class World:
    # simulaation maailma
    def __init__(self, side, beta1, beta2, alpha, pop, inf, scene):
        self.scene = scene
        self.beta1 = beta1  # kosketustartunnan todennäköisyys
        self.beta2 = beta2  # pisara(" = kauko")tartunnan tod.näk.
        self.alpha = alpha  # paranemistod.näk
        self.pop = pop  # populaatio
        self.inf = inf  # tartuttavat (HUOM tässä ohjelmassa termit Spreader ja inf/infectious tarkoittavat samaa)
        self.rec = 0  # parantuneiden määrä alussa nolla
        self.susc = pop - inf  # alttiit
        self.perished = 0
        self.am_of_cases = 0
        self.side = side
        self.squares = [None] * side
        for x in range(self.side):
            self.squares[x] = [None] * side
            for y in range(self.side):
                self.squares[x][y] = Square(Coordinates(x + 1, y + 1), self)

    def get_scene(self):
        return self.scene

    def get_side(self):
        return self.side

    def get_inf(self):
        return self.inf

    def get_rec(self):
        return self.rec

    def get_susc(self):
        return self.susc

    def get_cases(self):
        return self.am_of_cases

    def get_perished(self):
        return self.perished

    def change_inf(self, amount):
        # voi olla neg tai pos
        self.inf = self.inf + amount

    def change_rec(self):
        self.rec += 1

    def change_susc(self):
        self.susc -= 1

    def change_pop(self):
        self.pop -= 1
        self.perished += 1

    def change_cases(self):
        self.am_of_cases += 1

    def get_square(self, coords):
        return self.squares[coords.get_x() - 1][coords.get_y() - 1]

    def get_square_list(self):
        return self.squares

    def init_suscs(self):
        for i in range(self.susc):
            # arvo lähtöruutu
            x = random.randint(1, self.side)
            y = random.randint(1, self.side)
            curr_square = self.get_square(Coordinates(x, y))
            new = Susceptible(self, curr_square)
        self.susc = int(self.susc / 2)

    def init_infs(self):
        for i in range(self.inf):
            # nää on ne koordinaatit
            x = random.randint(1, self.side)
            y = random.randint(1, self.side)
            curr_square = self.get_square(Coordinates(x, y))
            new = Spreader(self, curr_square)
        self.inf = int(self.inf / 2)
