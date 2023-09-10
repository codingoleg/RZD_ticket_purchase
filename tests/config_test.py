import unittest

import config as cfg
from templates import templates


class TestConfig(unittest.TestCase):
    def test_mandatory_rzd(self):
        """Обязательные параметры РЖД"""
        self.assertIsInstance(cfg.username, str)
        self.assertIsInstance(cfg.password, str)
        self.assertIsInstance(cfg.date, str)
        self.assertIsInstance(cfg.departure_station, str)
        self.assertIsInstance(cfg.entry_station, str)
        self.assertIsInstance(cfg.adult_name, str)
        self.assertTrue(cfg.card_num.isdigit())
        self.assertTrue(cfg.card_exp.isdigit())
        self.assertTrue(cfg.card_cvv.isdigit())

    def test_mandatory_rzd_plaz(self):
        """Обязательные для плацкарта"""
        for seat_type in cfg.required_plaz_seat_types:
            self.assertIn(seat_type, templates.car_classes[templates.plazcart])
        self.assertIsInstance(cfg.bedding, bool)

    def test_mandatory_rzd_coupe(self):
        """Обязательные для купе"""
        for seat_type in cfg.required_plaz_seat_types:
            self.assertIn(seat_type, templates.car_classes[templates.coupe])
        self.assertIn(cfg.gender, {templates.man, templates.woman})

        if cfg.non_refundable:
            self.assertIn(any((templates.upper_last, templates.lower_last)),
                          cfg.required_coupe_seat_types)

    def test_optional_rzd(self):
        """Опциональные параметры РЖД"""
        self.assertIsInstance(cfg.child_name, str)
        self.assertIsInstance(cfg.rzd_bonus, str)
        self.assertIsInstance(cfg.non_refundable, bool)
        self.assertIsInstance(cfg.paramedic, bool)
        self.assertIsInstance(cfg.passenger_card_num, str)
        self.assertIsInstance(cfg.promocode, str)
        self.assertIn(cfg.reduced_fee_doc_type,
                      templates.reduced_fee_documents)
        self.assertIn(cfg.passenger_card_type, templates.passsenger_card_types)

    def test_optional_telegram(self):
        """Опциональные параметры телеграма"""
        self.assertIsInstance(cfg.bot, bool)
        if cfg.bot:
            self.assertIsInstance(cfg.TOKEN, str)
            self.assertTrue(cfg.TG_USER_ID.isdigit())


if __name__ == '__main__':
    unittest.main()
