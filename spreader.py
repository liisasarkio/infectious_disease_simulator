from direction import Direction
from coordinates import Coordinates
from recovered import Recovered
import susceptible
from brain import Brain
import brain_graphics


class Spreader(Brain):
    all_infs = []

    def __init__(self, world, square):
        super().__init__(world, square)
        self.days_since_infection = 0
        self.square.set_brain(self)
        self.nearest_hospital = 0
        self.define_nearest_hospital()  # määrittää tätä tartuttavaa lähinnä olevan sairaalan
        Spreader.all_infs.append(self)
        self.world.change_inf(1)
        self.world.change_cases()
        self.graphic = brain_graphics.BrainGraphicsItem(self, self.world.get_scene())  # tätä spreaderia kuvaava graphic item
        self.change_of_state = 0

    def define_nearest_hospital(self):
        x = self.square.get_x()
        y = self.square.get_y()
        if x > (self.world.get_side() / 2):
            if y <= (self.world.get_side() / 2):
                self.nearest_hospital = 2,
            elif y > (self.world.get_side() / 2):
                self.nearest_hospital = 4
        elif x <= (self.world.get_side() / 2):
            if y <= (self.world.get_side() / 2):
                self.nearest_hospital = 1
            elif y > (self.world.get_side() / 2):
                self.nearest_hospital = 3

    def move(self):
        # tämä metodi määrittää mihin suuntaan pitää liikkua
        # pyrkii aina liikkumaan kulmiin, joissa on sairaalat
        if self.nearest_hospital == 1:
            # ensin liikutaan x-suunnassa oikeaan kohtaan
            if self.square.get_x() > 1: # pitää liikkua länteen
                self.move_actually(3)
            # jos x-akselilla ollaan oikeassa kohdassa, liikutaan y-akselilla
            elif self.square.get_y() > 1: # pitää liikkua pohjoiseen
                self.move_actually(0)
            elif self.square.get_x() == 1 and self.square.get_y() == 1: # ollaan sairaalassa
                self.heal()
        elif self.nearest_hospital == 3:
            if self.square.get_x() > 1:  # pitää liikkua länteen
                self.move_actually(3)
            elif self.square.get_y() < self.world.get_side():  # pitää liikkua etelään
                self.move_actually(2)
            elif self.square.get_x() == 1 and self.square.get_y() == self.world.get_side():
                self.heal()
        elif self.nearest_hospital == 2:
            if self.square.get_x() < self.world.get_side():  # pitää liikkua itään
                self.move_actually(1)
            elif self.square.get_y() > 1:  # pitää liikkua pohjoiseen
                self.move_actually(0)
            elif self.square.get_x() == self.world.get_side() and self.square.get_y() == 1:
                self.heal()
        else:
            if self.square.get_x() < self.world.get_side():  # pitää liikkua itään
                self.move_actually(1)
            elif self.square.get_y() < self.world.get_side():  # pitää liikkua etelään
                self.move_actually(2)
            elif self.square.get_x() == self.world.get_side() and self.square.get_y() == self.world.get_side():
                self.heal()
        if self.change_of_state == 0:
            self.graphic.update_position()

    def increment_days(self):
        self.days_since_infection += 1

    def find_touch_suscs(self):
        susc_list = []
        brain_list = self.square.get_brains()
        for brain1 in brain_list:
            if isinstance(brain1, susceptible.Susceptible):
                susc_list.append(brain1)
        return susc_list

    def find_air_suscs(self):
        susc_list = []
        x = self.square.get_x()
        y = self.square.get_y()
        direction1 = Direction()
        list1 = direction1.get_all_directions()
        ilmansuunta = 0
        while ilmansuunta < 4:
            test_x = x + direction1.get_x_step(direction1, list1[ilmansuunta])
            test_y = y + direction1.get_y_step(direction1, list1[ilmansuunta])
            if not self.check_outside(test_x, test_y):
                test_square = self.world.get_square(Coordinates(test_x, test_y))
                for brain in test_square.get_brains():
                    if isinstance(brain, susceptible.Susceptible):
                        susc_list.append(brain)
            ilmansuunta += 1
        return susc_list

    def heal(self):
        self.change_of_state = 1
        Spreader.all_infs.remove(self)
        self.world.change_inf(-1)
        self.square.remove_brain(self)
        self.graphic.remove()  # poistetaan graphic item
        Recovered(self.world, self.square)

    def perish(self):
        self.change_of_state = 1
        Spreader.all_infs.remove(self)
        self.world.change_inf(-1)
        self.square.remove_brain(self)
        self.world.change_pop()
        self.graphic.remove()

