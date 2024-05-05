import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

FRIENDCHAT_DMS = """
CREATE TABLE IF NOT EXISTS chat_dms(
user1 TEXT,
user2 TEXT,
dm_id TEXT UNIQUE
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

c.execute(FRIENDCHAT_DMS)
c.execute(FRIENDCHAT_MESSAGES)

conn.commit()
conn.close()