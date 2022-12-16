import re
from datetime import datetime


def is_right_phone_number(phone_number):
    if len(phone_number) != 16:
        return False

    if phone_number[0] != "+" or phone_number[2] != "(":
        return False
    elif phone_number[6] != ")" or phone_number[10] != "-":
        return False
    elif phone_number[13] != "-":
        return False

    # +7(777)777-77-77
    idxs = [1, 3, 4, 5, 7, 8, 9, 11, 12, 14, 15]
    pattern = re.compile(r"[0-9]")

    for idx in idxs:
        if not re.fullmatch(pattern, phone_number[idx]):
            return False

    return True


def is_right_name(name):
    for symbol in name:
        if not (symbol.isalpha() or symbol == " "):
            return False

    return True


def is_right_gender(gender):
    return gender == "м" or gender == "ж"


def is_right_passport_num(passport_num):
    for num in passport_num:
        if not num.isdigit():
            return False

    return True


def is_right_date(date):
    if len(date) != 10:
        return False
    elif date[4] != '-' or date[7] != '-':
        return False
    else:
        for i in range(10):
            if i != 4 and i != 7 and not date[i].isdigit():
                return False

    return True


def is_right_time(time):
    if len(time) != 8:
        return False
    elif time.count(":") != 2:
        return False
    else:
        for i in time:
            if i == ":":
                continue
            if not i.isdigit():
                return False

        return True


def get_right_name(name):
    lst = list(map(str, name.split()))

    for i in range(len(lst)):
        lst[i] = lst[i].lower()
        lst[i] = lst[i][:1].upper() + lst[i][1:]

    return " ".join(lst)


def list_coincidence(lst1, lst2):
    flag1 = True
    flag2 = True

    for i in lst1:
        if not i in lst2:
            flag1 = False

    for i in lst2:
        if not i in lst1:
            flag2 = False

    return flag1 or flag2

def is_int(num):
    try:
        number = int(num)
    except Exception as e:
        return False
    return True


def is_right_password(password):
    symbols = "!@#$%&*"
    mp = {0: 0, 1:0, 2:0}

    for symb in password:
        if symb in symbols:
            mp[0] = 1
        elif symb.lower() == symb:
            mp[1] = 1
        elif symb.upper() == symb:
            mp[2] = 1

    return mp[0] and mp[1] and mp[2]


def is_right_category(category):
    categories = ["универсал", "внедорожник", "легковой", "минивэн", "спорткар"]

    return category.lower() in categories


def is_right_year(year):
    st_year = str(year)
    if len(year) != 4:
        return 0

    try:
        year = int(year)
        return (year >= 2000 and year <= 2022)
    except Exception as e:
        return 0


def is_right_transmission(transmission):
    transmissions = ["механика", "автомат"]
    print(transmission)
    return (transmission.lower() in transmissions)


def is_right_num(number):
    try:
        number = int(number)
        return number >= 0
    except Exception as e:
        return 0


def is_right_position(position):
    positions = ["администратор", "водитель", "продовец-консультант"]

    return  position in positions


def is_right_birth_day(birth_day):
    try:
        if len(birth_day) != 10:
            return False
        date = datetime.strptime(birth_day, "%Y-%m-%d")
        ds = (datetime.now()-date).days
        if ds > 23741 or ds < 6575:
            return False
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

print(is_right_birth_day("2002-12-03"))