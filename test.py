import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
create_table = "CREATE TABLE users (id integer, username text, password text)"

cursor.execute(create_table)
user = (1, 'jose', 'asdf')

insert_query = 'INSERT INTO users values (?, ?, ?)'
cursor.execute(insert_query, user)
connection.commit()
connection.close()