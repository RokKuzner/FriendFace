import sqlite3
import encryption

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

#Encrypt passwords
c.execute("SELECT * FROM users")
users = c.fetchall()

for user in users:
    password = user[2]
    id = user[1]
    c.execute('UPDATE users SET password=? WHERE id=?', (encryption.encrypt(password), id))

conn.commit()
conn.close()