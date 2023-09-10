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
        if templates.lower_last in cfg.required_plaz_seat_types \
                or templates.lower_last_module in cfg.required_plaz_seat_types:
            self.assertIn(templates.lower, cfg.required_plaz_seat_types,
                          'Должно быть добавлено templates.lower в '
                          'required_plaz_seat_types')
        if templates.upper_last in cfg.required_plaz_seat_types\
                or templates.upper_last_module in cfg.required_plaz_seat_types:
            self.assertIn(templates.upper, cfg.required_plaz_seat_types,
                          'Должно быть добавлено templates.upper в '
                          'required_plaz_seat_types')
        if templates.lower_side_toilet in cfg.required_plaz_seat_types:
            self.assertIn(templates.lower_side, cfg.required_plaz_seat_types,
                          'Должно быть добавлено templates.lower_side в '
                          'required_plaz_seat_types')
        if templates.upper_side_toilet in cfg.required_plaz_seat_types:
            self.assertIn(templates.upper_side, cfg.required_plaz_seat_types,
                          'Должно быть добавлено templates.upper_side в '
                          'required_plaz_seat_types')
        self.assertIsInstance(cfg.bedding, bool)

    def test_mandatory_rzd_coupe(self):
        """Обязательные для купе"""
        for seat_type in cfg.required_coupe_seat_types:
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
