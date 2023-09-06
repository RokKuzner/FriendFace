import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

USERS = """
CREATE TABLE IF NOT EXISTS users(
email TEXT UNIQUE,
id TEXT UNIQUE,
password TEXT,
friends TEXT
)
"""

POSTS = """
CREATE TABLE IF NOT EXISTS posts(
user TEXT,
content TEXT,
likes TEXT,
id TEXT UNIQUE
)
"""

c.execute(USERS)
c.execute(POSTS)

conn.commit()
conn.close()