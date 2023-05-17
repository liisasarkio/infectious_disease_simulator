from direction import Direction
from coordinates import Coordinates


class Brain:
    def __init__(self, world, square):
        self.world = world  # the world that the brain is a part of
        self.square = square  # the square where the brain is currently at

    def move_actually(self, num):
        # north = 0, east = 1, south = 2, west = 3
        direction_obj = Direction()
        direction_list = direction_obj.get_all_directions()
        curr_direction = direction_list[num]
        # set new square based on the direction
        new_x = self.square.get_x() + direction_obj.get_x_step(direction_obj, curr_direction)
        new_y = self.square.get_y() + direction_obj.get_y_step(direction_obj, curr_direction)
        # poistetaan omasta nykyisestä ruudustaan
        self.square.remove_brain(self)
        # asetetaan uuteen ruutuun
        new_square = self.world.get_square(Coordinates(new_x, new_y))
        self.square = new_square
        new_square.set_brain(self)

    def check_outside(self, test_x, test_y):
        # tämä metodi tarkastelee onko testikoordinaatit test_x ja test_y maailman ulkopuolella
        # palauttaa True jos on ulkopuolella, False jos ovat maailman sisäpuolella (testattu suunta/ruutu on ns. ok)
        if (test_x < 1 or test_x > self.world.get_side()) or (test_y < 1 or test_y > self.world.get_side()):
            return True
        else:
            return False

    def possible_directions(self, forbidden_list):
        # tämä metodi tuottaa listan sallituista ilmansuunnista, joista choice-metodi arpoo liikutun suunnan
        possible_list = []
        for i in range(4):
            if i not in forbidden_list:
                possible_list.append(i)
        return possible_list

