import sqlite3, random, string

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
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
    data = c.fetchone()
    return (data is not None and username == data[0] and password == data[2])


def add_user(username:str, password:str):
    c.execute('INSERT INTO users VALUES(?, ?, ?, ?)', (username, generate_id('users', 'id'), password, ''))
    conn.commit()
    return f'user {username} addded to db.'


def user_exists(username:str):
    c.execute('SELECT * FROM users WHERE email=?', (username, ))

    data = c.fetchone()

    return True if data is not None else False

def new_post(user:str, content:str):
    c.execute('INSERT INTO posts VALUES(?, ?, ?, ?, ?)', (user, content, "0", "", generate_id("posts", "id")))
    conn.commit()

def get_posts():
    c.execute('SELECT * FROM posts')
    return c.fetchall()

def get_posts_by_user(user:str):
    c.execute('SELECT * FROM posts WHERE user=?', (user,))
    return c.fetchall()

def like_post(user:str, post_id:str):
    if user_liked_post(user, post_id) != False:
        return None
    c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
    post =  c.fetchone()
    post_likes = int(post[2])
    post_user_likes = str(post[3]).split(',')

    new_post_user_likes = ''

    if post_likes == '0':
        new_post_user_likes = str(user)
    else:
        post_user_likes.append(user)
        new_post_user_likes = str(','.join(post_user_likes))

    post_likes += 1

    c.execute('UPDATE posts SET users_liked=?, likes=? WHERE id=?', (new_post_user_likes, str(post_likes), post_id))
    conn.commit()

def dislike_post(user:str, post_id:str):
    if user_liked_post(user, post_id) != True:
        return None
    c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
    post =  c.fetchone()
    post_likes = int(post[2])
    post_user_likes = str(post[3]).split(',')

    new_post_user_likes = ''

    post_user_likes.remove(user)
    new_post_user_likes = str(','.join(post_user_likes))
    post_likes -= 1

    c.execute('UPDATE posts SET users_liked=?, likes=? WHERE id=?', (new_post_user_likes, str(post_likes), post_id))
    conn.commit()

def user_liked_post(user:str, post_id:str):
    c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
    post = c.fetchone()

    post_user_likes = str(post[3]).split(',')

    return True if user in post_user_likes else False

def new_comment(user:str, content:str, parrent_post_id:str):
    c.execute('INSERT INTO comments VALUES(?, ?, ?, ?)', (user, content, parrent_post_id, generate_id("comments", "id")))
    conn.commit()


def get_comments_by_parrent_post(parrent_post_id:str):
    c.execute('SELECT * FROM comments WHERE parrent_id=?', (parrent_post_id,))
    return c.fetchall()