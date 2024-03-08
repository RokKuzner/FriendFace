import sqlite3
import keywordextractor as keyex

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

CREATE_KEYWORDS_COLUMN = """
ALTER TABLE posts ADD keywords TEXT;
"""
c.execute(CREATE_KEYWORDS_COLUMN)

c.execute('SELECT * FROM posts')
posts = c.fetchall()

for post in posts:
    if post[6] == None:
        post_keywords = keyex.extract_keywords(post[1])
        c.execute('UPDATE posts SET keywords=? WHERE id=?', (",".join(post_keywords), post[4]))
        conn.commit()

conn.commit()
conn.close()