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
id TEXT UNIQUE,
time TEXT,
keywords TEXT
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

POST_GENRE = """
CREATE TABLE IF NOT EXISTS postgenre(
postid TEXT UNIQUE,
genre TEXT
)
"""

USER_INTERESTS = """
CREATE TABLE IF NOT EXISTS interests(
user TEXT UNIQUE,
interests TEXT
)
"""

READ_POSTS = """
CREATE TABLE IF NOT EXISTS readposts(
user TEXT,
post TEXT
)
"""

DELETED_POSTS = """
CREATE TABLE IF NOT EXISTS deletedposts(
user TEXT,
content TEXT,
likes TEXT,
users_liked TEXT,
id TEXT,
time TEXT
)
"""

ADMIN_USERS = """
CREATE TABLE IF NOT EXISTS adminusers(
email TEXT UNIQUE,
id TEXT UNIQUE,
password TEXT,
roles TEXT
)
"""

KEYWORDS = """
CREATE TABLE IF NOT EXISTS keywords(
keyword TEXT UNIQUE,
posts TEXT
)
"""

FRIENDCHAT_DMS = """
CREATE TABLE IF NOT EXISTS chat_dms(
user1 TEXT,
user2 TEXT,
dm_id TEXT UNIQUE,
last_activity TEXT
)
"""

FRIENDCHAT_MESSAGES = """
CREATE TABLE IF NOT EXISTS chat_msgs(
dm_id TEXT,
message_id TEXT UNIQUE,
sender TEXT,
time TEXT,
content TEXT
)
"""

c.execute(USERS)
c.execute(POSTS)
c.execute(COMMENTS)
c.execute(POST_GENRE)
c.execute(USER_INTERESTS)
c.execute(READ_POSTS)
c.execute(DELETED_POSTS)
c.execute(ADMIN_USERS)
c.execute(KEYWORDS)
c.execute(FRIENDCHAT_DMS)
c.execute(FRIENDCHAT_MESSAGES)

conn.commit()
conn.close()