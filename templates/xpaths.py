import config as cfg

# find_tickets
def car_path(car):
    return f"//span[contains(text(), '{car}')]"


def seat_path(seat):
    return f"//span[contains(text(), 'Место {seat}')]"


continue_btn = "//button[@class='button--terminal']"


# initial_search
def choose_station_menu(station):
    return f"//li[@aria-label='{station}']"


direction_from_field = 'direction-from'
direction_to_field = 'direction-to'
datepicker_from_field = 'datepicker-from'
find_btn = "//a[@class='rzd-button bg-accessible rzd-go-to-result-button']"


# find_car_class
def choose_car_class(required_car_class):
    return f"//div[contains(text(), '{required_car_class}')]"


train_card = "//rzd-search-results-card-railway-flat-card"
search_result_bar = "//div[@class='searchresults']"
train_seat_types = "//div[@class='text-nowrap pricing-place-info__content" \
               "__description']"

# # Эти пути начинаются с точки. Поиск будет происходить только внутри.
car_class_names = ".//div[@class='card-class__name']"
train_num = ".//h3[@class='card-header__title ng-star-inserted']"
carrier = ".//span[@class='card-header__carrier']"


# login
def input_aria(field: str):
    return f"//input[@aria-label='{field}']"


sign_in_btn = "//a[@class='common-link tst-uiBtnAuthorization1']"
login = input_aria('Логин')
password = input_aria('Пароль')


# boarding
def passenger_dropdown(passenger_type):
    return f"//rzd-boarding-passenger-form-fields[@formgroupname='" \
           f"{passenger_type}']/div/div/ui-kit-form-field/div/div[" \
           f"@class='ui-kit-form-field__content']"


def adult_field(adult_name):
    return f"//div[contains(text(), '{adult_name}')]"


adult_boarding_data = 'passengerBoardingData'
kid_boarding_data = 'kidBoardingData'
non_refundable = "//ui-kit-checkbox[@formcontrolname='isNonRefundable']"
non_refundable_checkbox = f"{non_refundable}/div/input"
bedding = "//ui-kit-checkbox[@formcontrolname='isBeddingIncluded']"
bedding_checkbox = f"{bedding}/div/input"
child = "//ui-kit-checkbox[@formcontrolname='isAKidOnBoard']"
child_checkbox = f"{child}/div/input"
child_name = f"//div[contains(text(), '{cfg.child_name}')]"
boarding_summary = "//div[@class='boarding-summary']"


# choose_priveleges
def reduced_fee_document(document: str):
    return f"//div[contains(text(), '{document}')]"


def passenger_card(card_type: str):
    return f"//div[contains(text(), '{card_type}')]"


priveleges_panel = "//div[@class='bkit-expansion-panel__header']"
reduced_fee = "//ui-kit-select[@formcontrolname='privilegeOption']"
passenger_card_menu = "//ui-kit-select[@formcontrolname='passengerCard']"
passenger_card_add = "//div[contains(text(), 'Добавить новую карту')]"
passenger_card_menu_type = "//ui-kit-select[@formcontrolname='cardTypeOption']"
passenger_card_num = "//input[contains(@aria-label, 'Номер карты')]"
snils_field = input_aria('__boarding_privilege.snils_aria_label__')
deputy_field = input_aria('Введите номер удостоверения')
apply_fee = "//div[contains(text(),'Применить льготу')]"
rzd_bonus_field = "//input[contains(@aria-label, 'РЖД Бонус')]"
paramedic = "//ui-kit-checkbox[@formcontrolname='isParamedic']"
paramedic_checkbox = f"{paramedic}/div/input"
promocode_field = "//input[contains(@aria-label, 'Введите промокод ФПК')]"

# confirm_agreement
order_agreements = "//span[@class='order-agreements__text']"
pay_btn = "//div[contains(text(), 'Оплатить')]"

# enter_card
card_num_field = "//input[@id='cp-pan-decor']"
card_exp_field = "//input[@id='cc-exp-month']"
card_cvv_field = "//input[@id='cvv2']"
ok_btn = 'OK'

# enter_sms_code
sms_code_field = "//input[@id='passwordEdit']"

# __get_seats_info
# # Plaz
show_seats_list_btn = "//button[@aria-label='Для перехода к выбору " \
                      "мест нажмите Enter.']"
car_btn = "//span[contains(text(), 'Вагон')]"
seat_info_line_btn = "//div[@class='seat-card__title']"

# # Coupe
seat_type_btn = "//div[@class='seat-card__desc ng-star-inserted']"
