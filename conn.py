def create_connection(sqlite3):
    db = None
    try:
        # Название общего файла БД
        db = sqlite3.connect("the_main.db")
        # print(db)
    except Exception as e:
        print(e)
        return False

    return db