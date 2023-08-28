import sqlite3, random, string

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

def generate_id(table_name:str, id_field:str):

    while True:
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        c.execute(f'SELECT * FROM {table_name} WHERE {id_field}=?', (id, ))
        if c.fetchone() is None:
            break
        
    return id

def validate_user(username:str, password:str):
    c.execute('SELECT * FROM users WHERE email=? AND password=?',
              (username, password))
    return c.fetchone() is not None


def add_user(username:str, password:str):
    c.execute('INSERT INTO users VALUES(?, ?, ?)', (username, generate_id('users', 'id'), password))
    conn.commit()
    return f'user {username} addded to db.'


def user_exists(username:str):
    c.execute('SELECT * FROM users WHERE email=?', (username, ))

    if len(c.fetchall()) == 0:
        return False
    else:
        return True