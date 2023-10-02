import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

USERS = """
CREATE TABLE IF NOT EXISTS users(
email TEXT UNIQUE,
id TEXT UNIQUE,
password TEXT,
following TEXT,
followers TEXT,
followers_n TEXT
)
"""

POSTS = """
CREATE TABLE IF NOT EXISTS posts(
user TEXT,
content TEXT,
likes TEXT,
users_liked TEXT,
id TEXT UNIQUE
)
"""

COMMENTS = """
CREATE TABLE IF NOT EXISTS comments(
user TEXT,
content TEXT,
parrent_id TEXT,
id TEXT UNIQUE,
user_id TEXT
)
"""

c.execute(USERS)
c.execute(POSTS)
c.execute(COMMENTS)

conn.commit()
conn.close()