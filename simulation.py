from PyQt6 import QtWidgets, QtGui, QtCore
from world import World
from spreader import Spreader
from recovered import Recovered
from susceptible import Susceptible
import math
import random
from brain_graphics import BrainGraphicsItem


class Simulation(QtWidgets.QGraphicsScene):
    def __init__(self, view, window):
        # view on se GraphicsView, joka luodaan Window -luokassa, johon tämä Scene kuuluu
        super().__init__()
        self.view = view
        self.window = window
        self.square_size = 50  # gridin ruudun koko pikseleinä
        self.ret_list = self.ask_inputs()
        self.world = World(self.ret_list[0], self.ret_list[1], self.ret_list[2], self.ret_list[3], self.ret_list[4], self.ret_list[5], self)
        self.beta1 = self.ret_list[1]
        self.beta2 = self.ret_list[2]
        self.alpha = self.ret_list[3]
        # luodaan nappi
        self.button = QtWidgets.QPushButton("Edistä simulaatiota.")
        self.button.move(self.button.pos().x(), self.button.pos().y() - 50)
        self.addWidget(self.button)  # lisätään se sceneen
        self.button.clicked.connect(self.button_clicked)
        self.world.init_infs()
        self.world.init_suscs()

    def ask_inputs(self):
        # tämä metodi kysyy käyttäjältä simulaation alkutiedot
        print("Tervetuloa!\n")
        print("Keltainen = altis, punainen = tartuttava, vihreä = parantunut.")
        print("Kulmissa sairaalat, joissa tartuttavat paranevat varmasti.")
        print("Menehtyneet poistetaan simulaatiosta.\n")
        print("Simulaation maailma koostuu ruuduista.")
        side = int(input("Minkä parillisen kokonaisluvun haluat simulaation maailman sivun pituudeksi?\n"))
        while side % 2 != 0:
            print("Syötä parillinen luku.")
            side = int(input("Minkä parillisen kokonaisluvun haluat simulaation maailman sivun pituudeksi?\n"))
        tryagain = 0
        while tryagain == 0:
            try:
                pop = int(input("Kuinka suurelle populaatiolle simulaatio alustetaan?\n"))
                while pop <= 0:
                    print("Populaation tulee olla positiivinen luku.")
                    pop = int(input("Kuinka suurelle populaatiolle simulaatio alustetaan?\n"))
            except ValueError:
                print("Populaation tulee olla kokonaisluku.")
            tryagain = 1

        # sama juttu tartuttaville
        tryagain = 0
        while tryagain == 0:
            try:
                inf = int(input("Kuinka paljon tartuttavia henkilöitä on alkutilanteessa?\n"))
                while inf <= 0:
                    print("Määrän tulee olla positiivinen luku.")
                    inf = int(input("Kuinka paljon tartuttavia henkilöitä on alkutilanteessa??\n"))
            except ValueError:
                print("Määrän tulee olla kokonaisluku.")
            tryagain = 1

        # sitten todennäköisyydet
        beta1 = float(input("Mikä on todennäköisyys saada kyseinen tauti kosketustartunnalla?\n"))
        while beta1 <= 0 or beta1 > 1:
            print("Todennäköisyyden tulee olla luku nollan ja yhden väliltä")
            beta1 = float(input("Mikä on todennäköisyys saada kyseinen tauti kosketustartunnalla?\n"))
        beta2 = float(input("Mikä on todennäköisyys saada kyseinen tauti pisaratartunnalla?\n"))
        while beta2 <= 0 or beta2 > 1:
            print("Todennäköisyyden tulee olla luku nollan ja yhden väliltä")
            beta1 = float(input("Mikä on todennäköisyys saada kyseinen tauti pisaratartunnalla?\n"))
        alpha = float(input("Mikä on todennäköisyys parantua taudista?\n"))
        while alpha <= 0 or alpha > 1:
            print("Todennäköisyyden tulee olla luku nollan ja yhden väliltä")
            alpha = float(input("Mikä on todennäköisyys parantua taudista?\n"))
        return side, beta1, beta2, alpha, pop, inf

    def button_clicked(self):
        self.simulation_loop(self.beta1, self.beta2, self.alpha)

    def simulation_loop(self, beta1, beta2, alpha):
        # tässä metodissa tapahtuu varsinainen simulaatio
        # tämä yhdistetään GUI:n nappiin, jonka painaminen siis kutsuu tätä metodia

        if self.world.get_cases() < self.ret_list[4] and self.world.get_inf() != 0:
            # "päivä vaihtuu" -> PARANEMISET
            for spreaderbrain in Spreader.all_infs:
                spreaderbrain.increment_days()
                if spreaderbrain.days_since_infection == 4:
                    if random.random() < alpha:
                        spreaderbrain.heal()
                    else:
                        spreaderbrain.perish()

            # LIIKKUMINEN
            for alkio in Spreader.all_infs:
                alkio.move()
            for alkio1 in Recovered.all_recs:
                alkio1.move()
            for alkio2 in Susceptible.all_susc:
                alkio2.move()

                # TARTUTTAMINEN
                # tulee välttää sitä, ettei niistä, joihin nyt vasta tarttuu, tule heti itse tartuttavia
                # siksi luodaan ulkoiset 2D-listat total_*spread type*_susc, joille käydään tarttumistodennäköisyys läpi vasta
                # for loopin: "in range(world.get_inf())" jälkeen

                total_touch_susc = []
                total_air_susc = []
                # print(world.get_inf())
                # print(len(Spreader.all_infs))
                for n in range(self.world.get_inf()):
                    touch_susc_list = Spreader.all_infs[n].find_touch_suscs()
                    total_touch_susc.append(touch_susc_list)
                    air_susc_list = Spreader.all_infs[n].find_air_suscs()
                    total_air_susc.append(air_susc_list)
                for small_list in total_touch_susc:
                    # binomitodennäköisyys, pyöristetään ylöspäin
                    new_inf_amount = math.ceil((len(small_list) * beta1))
                    # koska kaikki tässä pikkulistassa ovat samassa ruudussa, ei ole väliä, mitkä kys. yksilöistä sairastuvat
                    # otetaan esimerkiksi ensimmäiset pikkulistasta
                    for i1 in range(new_inf_amount):
                        small_list[i1].fall_sick()
                for j1 in range(len(total_air_susc)):
                    for k1 in range(len(total_air_susc[j1])):
                        # todennäköisyys
                        if random.random() < beta2:  # sairastuu
                            total_air_susc[j1][k1].fall_sick()
        else:
            self.window.close()
            print("Tartuntojen määrä: {:d}".format(self.world.get_cases()))
            print("Menehtymisten määrä: {:d}".format(self.world.get_perished()))
