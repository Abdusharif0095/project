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
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    connection.close()

    if get_col_names:
        return rows, col_names
    else:
        return rows


connection = psycopg2.connect(
    database="test",
    user="abdusharif",
    password="abdu2002",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

try:
    cursor.execute("INSERT INTO Клиент VALUES(%s, %s, %s, %s, %s)", ("6", "Смирнова Наталья Андреевна", "88004653265", "4657409141", "ж"))
except Exception as e:
    print(e)

for row in get_data_from_dt("select * from Клиент;"):
    print(*row)