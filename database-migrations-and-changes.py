import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

CREATE_KEYWORDS_TABLE = """
CREATE TABLE IF NOT EXISTS keywords(
keyword TEXT UNIQUE,
posts TEXT
)
"""
c.execute(CREATE_KEYWORDS_TABLE)

c.execute('SELECT * FROM posts')
posts = c.fetchall()

keywords_dict = {}

for post in posts:
    post_keywords = post[6].split(",")
    for keyword in post_keywords:
        try:
            keywords_dict[keyword].append(post[4])
        except KeyError:
            keywords_dict[keyword] = [post[4]]

for keyword, posts in keywords_dict.items():
    c.execute('INSERT INTO keywords VALUES(?, ?)', (keyword, ",".join(posts)))

conn.commit()
conn.close()