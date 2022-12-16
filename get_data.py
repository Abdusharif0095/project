import psycopg2


def get_data_from_dt(query, get_col_names=False):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error: {e}")
        return [], [] if get_col_names else []
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    connection.close()

    if get_col_names:
        return rows, col_names
    else:
        return rows


def get_data_vals(query, vals, get_col_names=False):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query, tuple(vals))
    except Exception as e:
        print(f"Error: {e}")
        return []
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    connection.close()

    if get_col_names:
        return rows, col_names
    else:
        return rows


def update(query, values):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query, tuple(values))
        print("ok")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return []

    connection.commit()
    connection.close()

def insert(query, values):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query, tuple(values))
        connection.commit()
        connection.close()
        print("ok")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        connection.close()
        return 0


def delete(query, values):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
    except Exception as e:
        print(f"Error: {e}")
        return 0

    connection.commit()
    connection.close()
    return 1


def is_employee_in_base(fullname):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    query = "SELECT id, ФИО FROM Сотрудник;"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error: {e}")
        connection.close()
        return -1, False

    rows = cursor.fetchall()

    for row in rows:
        if fullname.lower() in row[1].lower():
            connection.close()
            return row[0], True

    connection.close()

    return -1, False


def is_client_in_base(fullname):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    query = "SELECT id, ФИО FROM Клиент;"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error: {e}")
        connection.close()
        return -1, False

    rows = cursor.fetchall()

    for row in rows:
        if fullname.lower() in row[1].lower():
            connection.close()
            return row[0], True

    connection.close()

    return -1, False


def is_auto_in_base(id):
    query = "SELECT * FROM Автомобиль WHERE id=%s;"
    values = [id]
    data = get_data_vals(query, values)

    return len(data) != 0

# print(is_auto_in_base(5))

def get_next_id(query):
    lst = get_data_from_dt(query)
    return int(lst[0][0]) + 1

def fix_soled_auto(id):
    query = "SELECT Количество FROM Автомобиль WHERE id=%s"
    values = [id]
    data = get_data_vals(query, values)
    cnt = int(data[0][0])

    if cnt > 0:
        query = "UPDATE Автомобиль SET Количество=%s WHERE id=%s;"
        values = [cnt-1, id]
        update(query, values)
        return 1
    else:
        return 0

def is_login_in_base(login, id):
    query = "SELECT * FROM Аутентификация;"
    data = get_data_from_dt(query)
    for row in data:
        if row[1].lower() == login.lower() and id != row[0]:
            return True
    return False


def save_log_pass(id, login, password):
    query = "UPDATE Аутентификация SET Логин=%s, password=%s WHERE idСотрудника=%s"
    values = [login, password, id]
    update(query, values)


def is_shipper_in_base(fullname):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    query = "SELECT id, Название FROM Поставщик;"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error: {e}")
        connection.close()
        return -1, False

    rows = cursor.fetchall()

    for row in rows:
        if fullname.lower() in row[1].lower():
            connection.close()
            print(f"id: {row[0]}")
            return row[0], True

    connection.close()

    return -1, False

