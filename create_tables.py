import sqlite3

def initDatabase():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username text, password text)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS items (id integer PRIMARY KEY, name text, price real)"
    cursor.execute(create_table)

    connection.commit()
    connection.close()
