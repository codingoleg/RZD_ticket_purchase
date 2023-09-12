import functools
import logging
import re
import time
from typing import Tuple, List, Callable

import config as cfg
import requests
import telebot
from templates import templates
from templates import xpaths as xp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

driver: webdriver
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

if cfg.bot:
    bot = telebot.TeleBot(token=cfg.TOKEN)
    logging.info('Телеграм бот запущен')
else:
    logging.info('Телеграм бот не запущен. Ввод смс-кода только через браузер')


def reload_error_page(train_func: Callable):
    """
    Обновить страницу, если любая из функций класса webdriver выдаст ошибку.
    Args:
        train_func: любая функция класса Train.
    Returns:
        class 'function'
    """

    @functools.wraps(train_func)
    def wrapper(*args) -> None:
        while True:
            try:
                train_func(*args)
            except WebDriverException:
                driver.refresh()
            else:
                break

    return wrapper


def alert_user(msg) -> None:
    """Логирование и отправка события в телеграм"""
    logging.info(msg)
    if cfg.bot:
        bot.send_message(cfg.TG_USER_ID, msg)


@reload_error_page
def start_driver() -> True:
    """Страртует webdriver с указанными настройками и получает URL.
    Работа headless не гарантируется - возможны ошибки."""
    global driver
    url_rzd = 'https://www.rzd.ru/'
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(url_rzd)
    alert_user('Запущена локальная версия webdriver')
    return True


def find_tickets(get_best_seat: Callable):
    """
    Args:
        get_best_seat: Поиск лучшего места для соответствующего класса вагона
    Returns:
        class 'function'
    """

    @functools.wraps(get_best_seat)
    def wrapper(self: Trains) -> bool:
        """Поиск билета нужного класса вагона (плацкарт, купе и т.д.).
        Если место найдено, выбирает лучшее.
        Args:
            self: подкласс класса Trains
        Returns:
            True, если место найдено.
            False, если место не найдено.
        """
        best_seat = get_best_seat(self)
        if not best_seat:
            return False
        alert_user(f'Лучшее место: {best_seat}')

        # Выбрать лучшие вагон и место
        car, seat = best_seat[0], best_seat[1]
        seat_path = xp.seat_path(seat)
        self.dfx(xp.car_path(car)).click()
        self.dfx(seat_path).location_once_scrolled_into_view
        self.click(self.dfx(seat_path))
        self.dfx(xp.continue_btn).click()
        return True

    return wrapper


class Trains:
    """Сокращение методов класса webdriver для лучшей читаемости"""

    @staticmethod
    def dfid(ID: str) -> webdriver:
        return driver.find_element(By.ID, ID)

    @staticmethod
    def dfx(xpath: str) -> webdriver:
        return driver.find_element(By.XPATH, xpath)

    @staticmethod
    def dfsx(xpath: str) -> webdriver:
        return driver.find_elements(By.XPATH, xpath)

    @staticmethod
    def waitpid(ID: str, sec=60) -> None:
        WebDriverWait(driver, sec).until(
            ec.presence_of_element_located((By.ID, ID)))

    @staticmethod
    def waitcx(xpath: str, sec=60) -> None:
        WebDriverWait(driver, sec).until(
            ec.element_to_be_clickable((By.XPATH, xpath)))

    @staticmethod
    def waitpx(xpath: str, sec=60) -> None:
        WebDriverWait(driver, sec).until(
            ec.presence_of_element_located((By.XPATH, xpath)))

    @staticmethod
    def click(element: webdriver) -> None:
        driver.execute_script("return arguments[0].click();", element)

    @staticmethod
    def run_scanner(car_classes: Tuple) -> True:
        """Запуск сканирования для всех указанных классов поездов."""
        while True:
            # Поиск для каждого класса поезда
            for car_class in car_classes:
                try:
                    if car_class.get_seat():
                        return True
                except WebDriverException:
                    pass
            driver.refresh()

    @reload_error_page
    def initial_search(self) -> True:
        """Поиск билетов со стартовой страницы с заданными параметрами:
        - Станция отправления
        - Станция прибытия
        - Дата отправления"""

        # Станция отправления
        self.waitpid(xp.direction_from_field)
        self.dfid(xp.direction_from_field).send_keys(cfg.departure_station)
        self.waitcx(xp.choose_station_menu(cfg.departure_station))
        self.dfx(xp.choose_station_menu(cfg.departure_station)).click()

        # Станция прибытия
        self.dfid(xp.direction_to_field).send_keys(cfg.entry_station)
        self.waitcx(xp.choose_station_menu(cfg.entry_station))
        self.dfx(xp.choose_station_menu(cfg.entry_station)).click()

        # Дата отправления
        self.dfid(xp.datepicker_from_field).send_keys(cfg.date)

        self.dfx(xp.find_btn).click()
        return True

    def find_car_class(
            self,
            required_car_class: str,
            required_car_seat_type: Tuple[str],
            excluded_trains: set,
            included_trains: set
    ) -> bool:
        """Ищет на странице выдачи желаемый класс вагона, наводя на него и
        исследуя содержимое всплывающего окна.
        Если в содержимом окна есть желаемый тип места, нажимает на него.
        Если желаемого типа места нет, переходит к следующему поезду.
        Args:
            included_trains: номера поездов, которые нужно включить в поиск.
            excluded_trains: номера поездов, которые нужно исключить из поиска.
            required_car_class: желаемый класс вагона.
            required_car_seat_type: желаемые типы мест в вагоне, начиная с
                самого приоритетного.
        Returns:
            True, если найден желаемый класс вагона и тип места в вагоне.
            False, если не найден.
        """

        # Завершить поиск, если класс вагона не найден ни в одном поезде
        try:
            self.waitcx(xp.choose_car_class(required_car_class))
        except TimeoutException:
            return False

        # Получаем список поездов
        trains = self.dfsx(xp.train_card)

        # Индекс нужен только для центрирования карточки поезда
        for index, train in enumerate(trains):

            # Получаем номер поезда и ищем во включённых и исключённых поездах
            train_num = train.find_element(By.XPATH, xp.train_num).text.strip()
            if train_num not in excluded_trains \
                    or train_num in included_trains:

                # Получаем название перевозчика. Если "ГРАНДТ", см. config.py
                carrier = train.find_element(By.XPATH, xp.carrier).text.strip()
                if carrier == templates.grandt and not cfg.include_grandt:
                    return False

                # Получаем названия классов вагона
                car_classes = train.find_elements(By.XPATH, xp.car_class_names)
                for car_class in car_classes:

                    # Проверяем соответствие класса вагона желаемому классу
                    if car_class.text == required_car_class:

                        # Центровка карточки, чтобы не закрывал footer/header
                        if index == 0:
                            center = self.dfx(xp.search_result_bar)
                        else:
                            center = trains[index - 1]
                        center.location_once_scrolled_into_view

                        # Наводим и ждем всплывающее окно с типами мест поезда
                        ActionChains(driver).move_to_element(
                            car_class).perform()
                        self.waitpx(xp.train_seat_types)

                        # Получаем названия типов мест вагона
                        seat_types = self.dfsx(xp.train_seat_types)
                        for seat_type in seat_types:

                            # Проверяем соответствие типов мест вагона желаемым
                            # типам мест
                            if seat_type.text in required_car_seat_type:

                                # Если перевозчик "ГРАНДТ", никуда не
                                # переходим. Если нет - переходим к выбору мест
                                found_msg = required_car_class + ' найден'
                                if carrier == templates.grandt:
                                    alert_user(found_msg + ' в ГРАНДТ')
                                else:
                                    alert_user(found_msg)
                                    car_class.click()
                                    return True

    @reload_error_page
    def login(self) -> True:
        """Авторизация после выбора билетов"""
        self.waitcx(xp.sign_in_btn)
        self.dfx(xp.sign_in_btn).click()
        self.dfx(xp.login).send_keys(cfg.username)
        self.dfx(xp.password).send_keys(cfg.password, Keys.ENTER)
        return True

    @reload_error_page
    def boarding(self) -> True:
        """Выбор пассажира, невозвратного тарифа, белья, ребенка"""
        non_refundable_error = 'Не удалось выбрать невозвратный тариф'
        non_refundable_added = 'Выбран невозвратный тариф'
        bedding_error = 'Не удалось выбрать постельное белье'
        child_error = 'Не удалось выбрать ребёнка'
        child_added = 'Ребенок добавлен'

        # Выбрать пассажира
        self.waitcx(xp.passenger_dropdown(xp.adult_boarding_data))
        self.dfx(xp.passenger_dropdown(xp.adult_boarding_data)).click()
        self.dfx(xp.adult_field(cfg.adult_name)).click()

        # Добавить невозвратный тариф.
        # Только для последнего купе класса "Купе". Не для всех поездов.
        try:
            self.dfx(xp.non_refundable).click()
        except NoSuchElementException:
            alert_user(non_refundable_error)
        else:
            alert_user(non_refundable_added)

        # Добавить/убрать постельное белье (только плацкарт)
        try:
            bedding_checkbox = self.dfx(
                xp.bedding_checkbox).get_attribute('aria-checked')
            if (cfg.bedding and bedding_checkbox == 'false') \
                    or (not cfg.bedding and bedding_checkbox == 'true'):
                self.dfx(xp.bedding).click()
        except NoSuchElementException:
            alert_user(bedding_error)

        # Добавить ребенка до 5 лет
        if cfg.child_name:
            try:
                self.dfx(xp.child).click()
                self.dfx(xp.passenger_dropdown(xp.kid_boarding_data)).click()
                self.dfx(xp.child_name).click()
            except NoSuchElementException:
                alert_user(child_error)
            else:
                alert_user(child_added)
        return True

    @reload_error_page
    def choose_priveleges(self) -> True:
        """Выбрать скидки/промокоды. Бронирование на 15 минут.
        Все пункты заполняются, но на данный момент нет возможности проверить
        работоспособность 0, 1 и 4 пунктов за неимением нужных документов.
        Порядковый номер привилегий:
        0: Льготный проезд и ВТТ
        1: Проездная карта
        2: РЖД Бонус
        3: Если пассажир медработник
        4: Скидки"""

        # Получаем список привилегий
        priveleges = self.dfsx(xp.priveleges_panel)

        if cfg.reduced_fee_doc_type and cfg.reduced_fee_doc_number:
            reduced_fee_btn = priveleges[0]
            reduced_fee_btn.click()
            self.dfx(xp.reduced_fee).click()
            self.dfx(xp.reduced_fee_document(cfg.reduced_fee_doc_type)).click()
            # Для удостоверения депутата
            if cfg.reduced_fee_doc_type == templates.deputy:
                self.dfx(xp.deputy_field).send_keys(cfg.reduced_fee_doc_number)
            else:
                self.dfx(xp.snils_field).send_keys(cfg.reduced_fee_doc_number)
            self.dfx(xp.apply_fee).click()

        if cfg.passenger_card_type:
            passenger_card_btn = priveleges[1]
            passenger_card_btn.click()

            # Добавить новую карту
            self.dfx(xp.passenger_card_menu).click()
            self.dfx(xp.passenger_card_add).click()

            # Выбрать карту
            self.dfx(xp.passenger_card_menu_type).click()
            self.dfx(xp.passenger_card(cfg.passenger_card_type)).click()
            self.dfx(xp.passenger_card_num).send_keys(cfg.passenger_card_num)

        if cfg.rzd_bonus:
            rzd_bonus_btn = priveleges[2]
            rzd_bonus_btn.click()
            self.dfx(xp.rzd_bonus_field).send_keys(cfg.rzd_bonus)

        if cfg.paramedic:
            paramedic_btn = priveleges[3]
            paramedic_btn.click()
            paramedic_checkbox = self.dfx(
                xp.paramedic_checkbox).get_attribute('aria-checked')
            if (cfg.paramedic and paramedic_checkbox == 'false') \
                    or (not cfg.paramedic and paramedic_checkbox == 'true'):
                self.dfx(xp.paramedic).click()

        if cfg.promocode:
            promocode_btn = priveleges[4]
            promocode_btn.click()
            self.dfx(xp.promocode_field).send_keys(cfg.promocode)

        self.dfx(xp.boarding_summary).location_once_scrolled_into_view
        self.dfx(xp.continue_btn).click()
        return True

    @reload_error_page
    def confirm_agreement(self) -> True:
        """Подтверждение 2 соглашений"""
        alert_user('Место забронировано. У вас есть 15 минут на оплату.')
        self.waitcx(xp.order_agreements)
        agreement_personal, agreement_3rd_party = self.dfsx(
            xp.order_agreements)

        '''Подтверждаю, что с правилами и особенностями оформления заказа,
        его оплаты, оформления и переоформления проездного документа
        (билета), возврата неиспользованного проездного документа (билета),
        заказанного через Интернет, изложенными в оферте, ознакомлен.'''
        agreement_personal.click()

        '''Настоящим подтверждаю, что в случае оформления мною проездных
        документов на третьих лиц, предоставляю персональные данные с их
        согласия.'''
        agreement_3rd_party.click()

        self.dfx(xp.pay_btn).click()
        return True

    @reload_error_page
    def enter_card(self) -> True:
        """Ввод реквизитов банковской карты: номер, истечение срока, CVV"""
        self.waitcx(xp.card_num_field)
        self.dfx(xp.card_num_field).send_keys(cfg.card_num)
        self.dfx(xp.card_exp_field).send_keys(cfg.card_exp)
        self.dfx(xp.card_cvv_field).send_keys(cfg.card_cvv)
        self.dfid(xp.ok_btn).click()
        alert_user('Введите код из смс для подтверждения')
        return True

    @reload_error_page
    def enter_sms_code(self) -> True:
        """Работает только при включенном боте. Ждём ввода кода из смс от
        пользователя в телеграм, чтобы вставить его в поле на сайте."""
        if cfg.bot:
            current_time = time.time()
            url_tg_updates = \
                f'https://api.telegram.org/bot{cfg.TOKEN}/getUpdates'
            while True:
                response = requests.post(url_tg_updates).json()
                time.sleep(5)
                try:
                    msg_info = response['result'][-1]['message']
                except IndexError:
                    # На случай, если у пользователя еще не было сообщений боту
                    pass
                else:
                    msg_from = str(msg_info['from']['id'])
                    msg_date = msg_info['date']
                    msg_text = msg_info['text']

                    # Находим последнее сообщение пользователя, которое позже
                    # по времени, чем последнее сообщение бота о вводе смс
                    if msg_date > current_time and msg_from == cfg.TG_USER_ID:
                        self.waitcx(xp.sms_code_field)
                        self.dfx(xp.sms_code_field).send_keys(msg_text,
                                                              Keys.ENTER)
                        return True


class Plaz(Trains):
    """Класс плацкарта"""

    def __get_seats_info(self) -> List[Tuple[str, int, float]]:
        """Получает информацию о свободных местах в вагоне.
        Returns:
            Каждый кортеж внутри списка имеет вид:
                (вагон: str, место: int, цена: float).
        """
        seats_info = []

        self.waitcx(xp.show_seats_list_btn)
        self.dfx(xp.show_seats_list_btn).click()

        # Получаем список вагонов
        cars = self.dfsx(xp.car_btn)
        for car in cars:
            car.click()
            # Получаем все доступные свободные места в вагоне
            seat_info_lines = self.dfsx(xp.seat_info_line_btn)
            for seat_info_line in seat_info_lines:
                seat = int(re.search('(\d+)', seat_info_line.text).group())
                price = float(seat_info_line.text.split()[2])
                seats_info.append((car.text.title(), seat, price))
        return seats_info

    @staticmethod
    def __create_seats_list() -> List[int]:
        """Добавляет в список номера мест, исходя из желаемых типов мест.
        Returns:
            Список номеров мест.
        """
        seats_list = []

        for seat_type in cfg.required_plaz_seat_types:
            # Эти типы мест уже включены в другие типы. Они нужны только для
            # сканера основной страницы.
            if seat_type in (
                templates.lower, templates.lower_side,
                templates.upper, templates.upper_side
            ):
                seats_list.extend(templates.plaz_seats[seat_type])
        return seats_list

    @find_tickets
    def __get_best_seat(self) -> Tuple[str, int, float]:
        """Получает лучший вагон и место плацкарта по шаблону выбора мест.
        Returns:
            Кортеж имеет вид: (вагон: str, место: int, цена: float).
        """
        seats_info = self.__get_seats_info()
        seats_list = self.__create_seats_list()
        for required_seat in seats_list:
            for seat in seats_info:
                free_seat = seat[1]
                if free_seat == required_seat:
                    return seat

    def get_seat(self):
        """Если место найдено, выбирает лучший вагон и место."""
        if self.find_car_class(
                required_car_class=templates.plazcart,
                required_car_seat_type=cfg.required_plaz_seat_types,
                excluded_trains=cfg.excluded_plaz,
                included_trains=cfg.included_plaz
        ):
            if self.__get_best_seat():
                return True


class Coupe(Trains):
    """Класс купе"""

    def __get_seats_info(self) -> List[Tuple[str, int, float, str]]:
        """Добавляем информацию о месте, если соблюдены оба условия:
        1) совпадает тип места с желаемым
        2) совпадает пол купе и пассажира, или гендерное купе отсутстввует
        Returns:
            Список кортежей информации о свободных местах в вагоне.
            Каждый кортеж внутри списка имеет вид:
                (вагон: str, место: int, цена: float, тип места: str).
        """
        seats_info = []

        self.waitcx(xp.show_seats_list_btn)
        self.dfx(xp.show_seats_list_btn).click()

        # Получаем список вагонов
        cars = self.dfsx(xp.car_btn)
        for car in cars:
            car.click()

            # Получаем все доступные свободные места в вагоне
            seat_info_lines = self.dfsx(xp.seat_info_line_btn)
            seat_types = self.dfsx(xp.seat_type_btn)
            for row, seat_info_line in enumerate(seat_info_lines):
                seat = int(re.search('(\d+)', seat_info_line.text).group())
                price = float(seat_info_line.text.split()[2])
                coupe_seat_type = seat_types[row].text
                if coupe_seat_type in cfg.required_coupe_seat_types:
                    if cfg.gender in seat_info_line.text or not any((
                            templates.man in seat_info_line.text,
                            templates.woman in seat_info_line.text
                    )):
                        seats_info.append((
                            car.text.title(), seat, price, coupe_seat_type))
        return seats_info

    @find_tickets
    def __get_best_seat(self) -> Tuple[str, int, float, str]:
        """
        Returns:
            Лучший вагон и место купе по очередности желаемых типов мест
        """
        seats_list = self.__get_seats_info()
        for coupe_seat_type in cfg.required_coupe_seat_types:
            for seat in seats_list:
                seat_type = seat[3]
                if seat_type == coupe_seat_type:
                    return seat

    def get_seat(self) -> True:
        """Если место найдено, выбрать лучший вагон и место."""
        if self.find_car_class(
                required_car_class=templates.coupe,
                required_car_seat_type=cfg.required_coupe_seat_types,
                excluded_trains=cfg.excluded_coupe,
                included_trains=cfg.included_coupe
        ):
            if self.__get_best_seat():
                return True
            else:
                alert_user('В поезде только несовпадающее купе по полу. '
                           'Добавьте номер поезда в исключенные поезда купе.')
