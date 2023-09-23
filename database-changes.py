import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

CHANGE = """
DROP TABLE posts;
"""

CHANGE2 = """
DROP TABLE users;
"""

CHANGE3 = """
DROP TABLE comments;
"""

c.execute(CHANGE)
c.execute(CHANGE2)
c.execute(CHANGE3)

conn.commit()
conn.close()