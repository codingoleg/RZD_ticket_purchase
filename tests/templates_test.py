import unittest
from templates.templates import *


class TestTemplates(unittest.TestCase):
    def test_plaz(self):
        """Валидность номеров плацкартных мест"""
        for seat in plaz_seats[lower]:
            assert 1 <= seat <= 36 and seat % 2
        for seat in plaz_seats[upper]:
            assert 1 <= seat <= 36 and not seat % 2
        for seat in plaz_seats[lower_side]:
            assert 37 <= seat <= 53 and seat % 2
        for seat in plaz_seats[upper_side]:
            assert 38 <= seat <= 54 and not seat % 2


if __name__ == '__main__':
    unittest.main()
