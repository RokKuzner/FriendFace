import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

CREATE_KEYWORDS_COLUMN = """
ALTER TABLE posts ADD keywords TEXT;
"""
c.execute(CREATE_KEYWORDS_COLUMN)

conn.commit()
conn.close()