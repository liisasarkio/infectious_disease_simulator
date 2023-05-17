import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView
from simulation import Simulation


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # asetetaan ikkunan koko
        self.setFixedWidth(1200)
        self.setFixedHeight(980)
        self.setWindowTitle('Tartuntatauti')
        self.init_simulation_gui()

    def init_simulation_gui(self):
        # luodaan view, scene (jota hoitaa toinen luokka Simulation), ja lopulta näytetään ikkuna
        self.view = QGraphicsView()
        self.scene = Simulation(self.view, self)
        # asetetaan view central widgetiksi
        self.setCentralWidget(self.view)
        self.view.setScene(self.scene)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

