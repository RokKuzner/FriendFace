import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

CHANGE = """
DROP TABLE posts;
"""

c.execute(CHANGE)

conn.commit()
conn.close()