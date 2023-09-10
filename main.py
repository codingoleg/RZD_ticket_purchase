"""
Основной скрипт.

car_classes: список классов поездов для поиска. Можно добавлять/удалять
    экземляры класса и изменять порядок. По умолчанию ищет плацкарт и купе:
    car_classes: Tuple = (Plaz(), Coupe()).
"""
from typing import Tuple

from trains import start_driver, Trains, Plaz, Coupe

car_classes: Tuple = (Plaz(), Coupe())

if __name__ == '__main__':
    # Запуск браузера.
    start_driver()

    # Поиск билетов со стартовой страницы с заданными параметрами
    train = Trains()
    train.initial_search()

    # Запуск сканирования для всех указанных классов поездов
    train.run_scanner(car_classes)

    # Авторизация после выбора билетов
    train.login()

    # Выбор пассажира, невозвратного тарифа, белья, ребенка
    train.boarding()

    # Выбор скидок/промокодов. Бронирование на 15 минут.
    train.choose_priveleges()

    # Подтверждение 2 соглашений
    train.confirm_agreement()

    # Ввод реквизитов банковской карты: номер, истечение срока, CVV
    train.enter_card()

    # Ввод кода из смс или пуш-уведомления от банка для оплаты билета
    train.enter_sms_code()
