""""
Конфигурация пользователя.

Обязательные параметры РЖД:
    username: логин РЖД.
    password: пароль РЖД.
    date: дата отправления формата DD.MM.YYYY.
    departure_station: станция отправления.
    entry_station: станция прибытия.
    adult_name: ФИО через пробел. ФИО должно точно соответствовать тому ФИО,
        которое указано у пассажира РЖД на сайте.
    card_num: номер карты без пробелов.
    card_exp: дата истечения срока карты без пробелов.
    card_cvv: CVV.
    include_grandt:
        True: будет сканировать перевозчика "ГРАНДТ" и оповещать, если билет
            найден, но его нужно будет покупать в ручном режиме.
            Сканирование продолжится.
        False: будет пропускать "ГРАНДТ".

            Перевозчик "ГРАНДТ" перенаправляет на другой сайт.
            Этот скрипт не предназначен для него.

    Плацкарт:
        Обязательные:
            bedding: постельное белье
            required_plaz_seat_types: желаемые типы мест плацкарта, начиная с
                более приоритетных. Все доступные типы мест есть в модуле
                ./templates/templates.py в переменной car_classes[plazcart].
                Обязательно должен включать в себя хотя бы один тип из списка:
                "Нижнее", "Верхнее", "Боковое нижнее", "Боковое верхнее".

        Опциональные:
            excluded_plaz: номера поездов, которые исключены из поиска.
            included_plaz: номера поездов, которые включены в поиск.

            Если оба параметра пустые (по умолчанию), то поиск будет
            происходить по всем поездам. Если хотя бы один параметр не пустой,
            то другой должен быть пустым.
            Пример:
                excluded_plaz = {'020У', '016А', '060*Г'}

    Купе:
        Обязательные:
            gender: пол пассажира в среднем роде с большой буквы.
                Доступные варианты: 'Мужское', 'Женское'.
            required_coupe_seat_types: желаемые типы мест купе, начиная с более
                приоритетных. Все доступные типы мест есть в модуле
                ./templates/templates.py в переменной car_classes[coupe].

        Опциональные:
            excluded_coupe: номера поездов, которые исключены из поиска.
            included_coupe: номера поездов, которые включены в поиск.

            Если оба параметра пустые (по умолчанию), то поиск будет
            происходить по всем поездам. Если хотя бы один параметр не пустой,
            то другой должен быть пустым.
            Пример:
                excluded_coupe = {'020У', '016А', '060*Г'}

            non_refundable: невозвратный тариф. Дает скидку в последнее купе.
                Доступен, только если добавлены 'Последнее купе, верхнее' или
                'Последнее купе, нижнее' в required_coupe_seat_types и есть
                соответствующие типы мест в поезде.

Опциональные параметры РЖД (строку оставить пустой, если параметр отсутствует):
    child_name: ФИО ребёнка через пробел. ФИО должно точно соответствовать тому
        ФИО, которое указано у ребёнка вна сайте.
    rzd_bonus: номер РЖД бонус.
    paramedic: является ли пассажир медиком.
    passenger_card_type: тип проездной карты. Все доступные типы есть в модуле
        ./templates/templates.py в переменной passsenger_card_types.
    passenger_card_num: номер проездной карты.
    promocode: промокод.
    reduced_fee_doc_type: основание получения льготы. Все доступные основания
        есть в модуле ./templates/templates.py в переменной
        reduced_fee_documents.
    reduced_fee_doc_number: номер СНИЛС или номер Удостоверения депутата ГД,
        в зависимости от параметра reduced_fee_doc_type.

Опциональные параметры телеграма:
    bot:
        True. Включить бота.
        False. Не включать бота. Уведомления не будут приходить, и смс код от
            банка можно будет ввести только напрямую в браузере.
    TOKEN = токен бота.
    TG_USER_ID = ID пользователя, кому отправлять уведомления.

Внимание!
    - Некоторые скидки не сочетаются друг с другом.
    - Некоторые скидки привязаны к указываемому номеру паспорта.
    - Некоторые скидки действуют не на всех перевозчиков.
    Рекомендуется проверить заранее работу скидок для того же поезда с другой
    датой отправления, либо для этого же поезда, но другого типа вагона.
"""

from typing import Tuple

from templates import templates

# Обязательные параметры РЖД
username: str = 'test_account_rzd'
password: str = '4zcnLR2FKp7'
date: str = '25.09.2023'  # ДД.ММ.ГГГГ
departure_station: str = 'Москва'
entry_station: str = 'Санкт-Петербург'
adult_name: str = 'Фамилия Имя Отчество'
card_num: str = '4276380113854744'
card_exp: str = '1023'
card_cvv: str = '123'
include_grandt: bool = True

# # Обязательные для плацкарта
bedding: bool = True
required_plaz_seat_types: Tuple = (
    templates.lower,
    templates.lower_last,
    templates.lower_last_module,
    templates.lower_side,
    templates.lower_side_toilet,
    templates.upper,
    templates.upper_last,
    templates.upper_last_module,
    templates.upper_side,
    templates.upper_side_toilet,
)

# # Опциональные для плацкарта
excluded_plaz: set[str] = set()
included_plaz: set[str] = set()

# # Обязательные для купе
gender: str = templates.man
required_coupe_seat_types: Tuple = (
    templates.lower,
    templates.lower_last,
    templates.upper,
    templates.upper_last,
)

# # Опциональные для купе
excluded_coupe: set[str] = set()
included_coupe: set[str] = set()
non_refundable = False

# Опциональные параметры РЖД
child_name: str = 'Иванов Андрей Петрович'
rzd_bonus: str = ''
paramedic: bool = False
passenger_card_type: str = ''
passenger_card_num: str = ''
promocode: str = ''
reduced_fee_doc_type: str = ''
reduced_fee_doc_number: str = ''

# Опциональные параметры телеграма
bot: bool = False
TOKEN: str = 'ВАШ ТОКЕН'
TG_USER_ID: str = 'ID пользователя'
