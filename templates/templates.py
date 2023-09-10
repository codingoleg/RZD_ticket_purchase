# Классы вагона
base = 'Базовый'
base_incapacitated = 'Базовый (для инвалидов)'
business_class = 'Бизнес класс'
business_coupe = 'Бизнес-купе'
car_bistro = 'Вагон-бистро'
coupe = 'Купе'
coupe_conference = 'Купе-переговорная'
coupe_incapacitated = 'Купе (для инвалидов)'
coupe_suite = 'Купе-сьют'
family = 'Семейный'
first_class = 'Первый класс'
economy = 'Эконом'
economy_incapacitated = 'Эконом (для инвалидов)'
economy_plus = 'Эконом+'
lux = 'Люкс'
plazcart = 'Плацкартный'
sitting = 'Сидячий'
sleeping_car = 'СВ'

# Содержание классов
coupe_incapacitated_lower = 'Для инвалидов, нижнее'
coupe_accompanying = 'Для сопровождающих'
incapacitated = 'Для инвалидов'
lower = 'Нижнее'
lower_last = 'Последнее купе, нижнее'
lower_last_module = 'Последнее купе (отсек), нижнее'
lower_side = 'Боковое нижнее'
lower_side_toilet = 'Боковое нижнее у туалета'
mother_and_child = 'Для матери и ребенка'
regular_seat = 'Обычное место'
single_forward = 'Одиночное, по ходу'
sitting_incapacitated = 'Сидячий (для инвалидов)'
table = 'У стола'
table_backward = 'У стола, против хода'
table_forward = 'У стола, по ходу'
upper = 'Верхнее'
upper_last = 'Последнее купе, верхнее'
upper_last_module = 'Последнее купе (отсек), верхнее'
upper_side = 'Боковое верхнее'
upper_side_toilet = 'Боковое верхнее у туалета'
without_table_forward = 'Не у стола, по ходу'
without_table_backward = 'Не у стола, против хода'
without_window_forward = 'Без окна, по ходу'
without_window_backward = 'Без окна, против хода'
with_animal = 'Для пассажира с животным'
with_animals = 'С животными'
with_children = 'Для пассажира с детьми'

# Структура классов
car_classes = {
    base: (
        table_forward,
        table_backward,
        without_window_forward,
        without_window_backward,
        without_table_forward,
        without_table_backward,
        with_animal,
        with_animals,
    ),
    base_incapacitated: (
        incapacitated,
    ),
    business_class: (
        table_forward,
        table_backward,
        without_table_forward,
        without_table_backward,
    ),
    business_coupe: (
        regular_seat,
    ),
    car_bistro: (
        table_forward,
        table_backward,
    ),
    coupe: (
        lower,
        lower_last,
        upper,
        upper_last,
    ),
    coupe_conference: (
        regular_seat,
    ),
    coupe_incapacitated: (
        coupe_incapacitated_lower,
        coupe_accompanying,
    ),
    coupe_suite: (
        regular_seat,
    ),
    economy: (
        table_forward,
        table_backward,
        without_table_forward,
        without_table_backward,
        without_window_forward,
        without_window_backward,
        with_animal,
        with_animals,
    ),
    economy_incapacitated: (
        incapacitated,
    ),
    economy_plus: (
        table_forward,
        table_backward,
        without_table_forward,
        without_table_backward,
        with_children,
        mother_and_child,
    ),
    family: (
        without_table_backward,
        with_children,
    ),
    first_class: (
        without_table_forward,
        without_table_backward,
        single_forward,
    ),
    lux: (
        regular_seat,
    ),
    plazcart: (
        lower,
        lower_last,
        lower_last_module,
        lower_side,
        lower_side_toilet,
        upper,
        upper_last,
        upper_last_module,
        upper_side,
        upper_side_toilet,
    ),
    sitting: (
        table,
        regular_seat,
        with_children,
    ),
    sitting_incapacitated: (
        incapacitated,
    ),
    sleeping_car: (
        lower,
    ),
}

# Перевозчики
fpk = 'ФПК'
grandt = 'ГРАНДТ'
tversk = 'ТВЕРСК'

'''
Здесь представлены все места. Порядок мест в плацкарте идет от лучших мест 
в центре вагона до худших по краям. Остальные места ('Боковое нижнее у 
туалета', 'Последнее купе, верхнее', 'Последнее купе, нижнее', 'Последнее купе 
(отсек), верхнее', 'Последнее купе (отсек), нижнее') уже включены в имеющиеся. 
На сайте РЖД не всегда правильно подписаны места, поэтому пришлось оставить 
только основные 4 группы. При необходимости, можно поменять порядок.
'''
plaz_seats = {
    lower: (17, 19, 13, 15, 21, 23, 9, 11, 25,
            27, 5, 7, 1, 3, 29, 31, 33, 35),
    upper: (18, 20, 14, 16, 22, 24, 10, 12, 26,
            28, 6, 8, 2, 4, 30, 32, 34, 36),
    lower_side: (45, 47, 43, 49, 41, 51, 53, 39, 37),
    upper_side: (46, 48, 44, 50, 42, 52, 54, 40, 38),
}

# Пол
man = 'Мужское'
woman = 'Женское'

# Скидки
etfss = 'ЭТФСС'
vtt = 'ВТТ'
etminsoc = 'ЭТМИНСОЦ'
deputy = 'Удостоверение депутата ГД'
reduced_fee_documents = (etfss, vtt, etminsoc, deputy, '')
delovoy_proezdnoy = 'Деловой проездной'
discount_card = 'Скидочная карта'
gift_card = 'Подарочная карта'
passsenger_card_types = (delovoy_proezdnoy, discount_card, gift_card, '')
