import sqlite3
import time
from conn import create_connection

now = round(time.time())
a_year = 3600 * 24 * 365  # in a seconds


def clean_users():
    records = []
    n = 0
    try:
        database = create_connection(sqlite3)
        cursor_key = database.cursor()
        sql_key = f'SELECT chat_id, date FROM users_table WHERE active = 1'
        cursor_key.execute(sql_key)
        records = cursor_key.fetchall()
    except sqlite3.Error as error:
        print("Ошибка подключения 1", error)
    if records:
        for row in records:
            if now < row[1] + a_year:
                pass
            else:
                n +=1
                db = create_connection(sqlite3)
                cursor = db.cursor()
                sql1 = f"UPDATE users_table SET active = 0 WHERE chat_id = ? "
                cursor.execute(sql1, (row[0],))
                db.commit()
                db.close()
        return print(f"I cleaned a {n}")
    else:
        return print(f"Nothing to clean")