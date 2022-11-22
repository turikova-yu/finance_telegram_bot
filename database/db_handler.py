import sqlite3

def get_cursor(query : str) -> sqlite3.Cursor:
    with sqlite3.connect('database/finance.db') as con:
        """ Выполнить запрос query  и вернуть курсор """
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        return cursor


