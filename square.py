from coordinates import Coordinates
from PyQt6 import QtWidgets, QtGui, QtCore

class Square:
    def __init__(self, coords, world):
        self.coordinates = coords
        self.brains = [] # brainit jotka ovat parhaillaan ruudussa
        self.world = world
        # seuraava rivi luo jokaisesta Squaresta graafisen ilmentymän, joista simulaation ruudukko sitten koostuu
        self.square_graphic = QtWidgets.QGraphicsRectItem((self.get_x() - 1) * 50, (self.get_y() - 1) * 50, 50, 50)
        # luodaan vielä QRectF olio tästä Squaresta, jota voidaan käyttää kun luodaan BrainGraphicsItemeitä
        self.square_f = QtCore.QRectF((self.get_x() - 1) * 50, (self.get_y() - 1) * 50, 50, 50)
        if (self.get_x() == 1 and (self.get_y() == 1 or self.get_y() == self.world.get_side())) or (
                self.get_x() == self.world.get_side() and (self.get_y() == 1 or self.get_y() == self.world.get_side())):
            self.square_graphic.setBrush(QtGui.QColor(20, 20, 20))  # tämä Square on kulma
        else:
            self.square_graphic.setBrush(QtGui.QColor(211, 211, 211))
        self.world.get_scene().addItem(self.square_graphic)

    def get_square_f(self):
        return self.square_f

    def get_x(self):
        return self.coordinates.get_x()

    def get_y(self):
        return self.coordinates.get_y()

    def get_brains(self):
        return self.brains

    def set_brain(self, brain):
        self.brains.append(brain)

    def remove_brain(self, brain):
        self.brains.remove(brain)
