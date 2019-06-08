import sqlite3

with sqlite3.connect("Login.db") as db:
    cursor = db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS user(
username VARCHAR(20) PRIMARY KEY,
password VARCHAR(20) NOT NULL);""")

cursor.execute("""
INSERT INTO user (username,password)
VALUES("p1", "123")
""")

cursor.execute("""
INSERT INTO user (username,password)
VALUES("p2", "111")
""")

db.commit()

cursor.execute("SELECT * FROM user")
#just to make sure the right things are input
print (cursor.fetchall())