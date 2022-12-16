import psycopg2


def get_data_vals(query, vals, get_col_names=False):
    connection = psycopg2.connect(
        database="test",
        user="abdusharif",
        password="abdu2002",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute(query, tuple(vals))
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    connection.close()

    if get_col_names:
        return rows, col_names
    else:
        return rows