from PyQt6 import QtWidgets, QtGui
import susceptible
import spreader
import recovered


class BrainGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, brain, scene):
        super(BrainGraphicsItem, self).__init__()
        self.brain = brain
        self.square_size = 50
        # scene, johon graphics item kuuluu
        self.scene = scene
        brush = QtGui.QBrush(1)
        self.setBrush(brush)
        self.scene.addItem(self)
        self.make_circle()

    def make_circle(self):
        # annetaan ellipsille suorakulmioksi(neliöksi) sen Squaren, jossa brain sijaitsee, QRectF -item
        self.setRect(self.brain.square.get_square_f())

        # asetetaan väri
        if isinstance(self.brain, susceptible.Susceptible):
            # keltainen
            self.setBrush(QtGui.QColor(255, 255, 0))
        elif isinstance(self.brain, spreader.Spreader):
            # punainen
            self.setBrush(QtGui.QColor(255, 0, 0))
        elif isinstance(self.brain, recovered.Recovered):
            # vihreä
            self.setBrush(QtGui.QColor(0, 255, 0))

    def update_position(self):
        # nykyisen (uuden) ruudun eli Squaren QRectF -item
        self.setRect(self.brain.square.get_square_f())
        self.update()

    def remove(self):
        self.scene.removeItem(self)
