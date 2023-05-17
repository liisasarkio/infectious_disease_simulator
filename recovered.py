import random
from direction import Direction
from coordinates import Coordinates
from brain import Brain
import brain_graphics


class Recovered(Brain):
    all_recs = []
    # näiden määrä ei voi kuin vain lisääntyä

    def __init__(self, world, square):
        super().__init__(world, square)
        self.all_recs.append(self)
        self.square.set_brain(self)
        self.world.change_rec()
        self.graphic = brain_graphics.BrainGraphicsItem(self, self.world.get_scene())  # tätä recoveredia kuvaava graphic item

    def move(self):
        # liikkuu sattumanvaraisesti
        # arvotaan suunta mihin liikkuu
        num = random.randint(0, 3)
        forbidden = []
        direction_obj = Direction()
        direction_list = direction_obj.get_all_directions()
        curr_direction = direction_list[num]
        # set new square based on the direction
        new_x = self.square.get_x() + direction_obj.get_x_step(direction_obj, curr_direction)
        new_y = self.square.get_y() + direction_obj.get_y_step(direction_obj, curr_direction)
        # tutkitaan onko testiruutu maailman ulkopuolella
        while self.check_outside(new_x, new_y):
            forbidden.append(num)
            num = random.choice(self.possible_directions(forbidden))
            curr_direction = direction_list[num]
            new_x = self.square.get_x() + direction_obj.get_x_step(direction_obj, curr_direction)
            new_y = self.square.get_y() + direction_obj.get_y_step(direction_obj, curr_direction)
        # poistetaan omasta nykyisestä ruudustaan
        self.square.remove_brain(self)
        # asetetaan uuteen ruutuun
        new_square = self.world.get_square(Coordinates(new_x, new_y))
        self.square = new_square
        new_square.set_brain(self)
        # päivitetään graphic itemin sijainti
        self.graphic.update_position()
