import random
from coordinates import Coordinates
from square import Square
from direction import Direction
import spreader
from brain import Brain
import brain_graphics


class Susceptible(Brain):
    all_susc = []

    def __init__(self, world, square):
        super().__init__(world, square)
        self.square.set_brain(self)
        self.all_susc.append(self)
        self.world.change_susc()
        self.graphic = brain_graphics.BrainGraphicsItem(self, self.world.get_scene())  # tätä spreaderia kuvaava graphic item

    def move(self):
        # liikkuu aina tyhjään ruutuun jos mahd.
        # tämä metodi määrittää mihin suuntaan liikutaan
        x = self.square.get_x()
        y = self.square.get_y()
        direction1 = Direction()
        list1 = direction1.get_all_directions()
        ilmansuunta = 0
        end_search = 0
        forbidden = []
        while ilmansuunta < 4 and end_search == 0:
            test_x = x + direction1.get_x_step(direction1, list1[ilmansuunta])
            test_y = y + direction1.get_y_step(direction1, list1[ilmansuunta])
            # tutkitaan onko testiruutu maailman ulkopuolella
            if self.check_outside(test_x, test_y):
                forbidden.append(ilmansuunta)
            else:
                test_square = self.world.get_square(Coordinates(test_x, test_y))
                if len(test_square.get_brains()) == 0:  # ruutu on tyhjä // ja sallittu eli ei tarvi miettii kielletyt
                    self.move_actually(ilmansuunta)
                    end_search = 1
            ilmansuunta += 1
        if end_search == 0:  # mikään ruutu ei ollut tyhjä
            if len(forbidden) == 0:
                self.move_actually(random.randint(0, 3))
            else:
                self.move_actually(random.choice(self.possible_directions(forbidden)))
        self.graphic.update_position()

    def fall_sick(self):
        Susceptible.all_susc.remove(self)
        self.world.change_susc()
        self.square.remove_brain(self)
        self.graphic.remove()
        spreader.Spreader(self.world, self.square)
