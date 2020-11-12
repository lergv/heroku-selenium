import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

c.execute("""CREATE TABLE customer (
        id integer,
        content text,
        completed integer,
        data_created text
        )""")

conn.commit()

conn.close()