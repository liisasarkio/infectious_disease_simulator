import unittest
from world import World
import spreader
from coordinates import Coordinates
from PyQt6 import QtWidgets

# pari huomiota:
# tämä toki luottamuksenvaraista, mutta nämä testit toimi/"meni läpi" ennen kuin implementoin graafisen käyttöliittymän
# saattaa toki johtua jostain muustakin, mutta nyt testeihin tulee nollasta eroava exit code, kun ne ajaa.


class Test(unittest.TestCase):
    def setUp(self):
        self.testworld = World(6, 0.7, 0.4, 0.9, 6, 2, QtWidgets.QGraphicsScene())
        self.testworld.init_infs()
        testspreader1 = spreader.Spreader(self.testworld, self.testworld.get_square(Coordinates(3, 3)))

    def test_inf_amounts(self):
        self.assertEqual(len(spreader.Spreader.all_infs), self.testworld.get_inf())

    def test_check_outside(self):
        testspreader1 = spreader.Spreader(self.testworld, self.testworld.get_square(Coordinates(3, 3)))
        retval1 = testspreader1.check_outside(0, 0)
        retval2 = testspreader1.check_outside(2, 2)
        self.assertTrue(retval1)
        self.assertFalse(retval2)


if __name__ == "__main__":
    unittest.main()


