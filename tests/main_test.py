import unittest

from main import car_classes
from trains import Trains


class TestMain(unittest.TestCase):
    def test_car_classes(self):
        for class_ in car_classes:
            self.assertIsInstance(
                class_, Trains, 'Класс должен быть подклассом Trains')


if __name__ == '__main__':
    unittest.main()
