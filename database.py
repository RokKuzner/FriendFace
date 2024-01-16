import sqlite3, random, string, time
import algorythms as alg

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)

def generate_id(table_name:str, id_field:str):
    with conn:
        c = conn.cursor()
        while True:
            id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            c.execute(f'SELECT * FROM {table_name} WHERE {id_field}=?', (id, ))
            if c.fetchone() is None:
                break
            
        return id

#Users
def validate_user(username:str, password:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=? AND password=?',
                (username, password))
        data = c.fetchone()
        return (data is not None and username == data[0] and password == data[2])

def add_user(username:str, password:str):
    with conn:
        c = conn.cursor()
        user_id = generate_id('users', 'id')
        c.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)', (username, user_id, password, '', '', '0'))
        c.execute('INSERT INTO interests VALUES(?, ?)', (username, ""))
        conn.commit()
        return user_id

def get_users_id_by_username(username:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (username,))
        data = c.fetchone()

        return data[1] if data != None else None

def user_exists(username:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (username, ))

        data = c.fetchone()

        return True if data is not None else False

def is_following_user(user_following:str, user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (user_following,))
        returned = c.fetchone()

        if returned == None or returned[3] == '':
            return False
        else:
            user_following_list = str(returned[3]).split(',')
            return True if user in user_following_list else False

def follow_user(user_following:str, user_to_follow:str):
    with conn:
        c = conn.cursor()
        if is_following_user(user_following, user_to_follow) == True:
            return "User allready following"
        
        if user_following == user_to_follow:
            return "Cannot subscribe to yourself"
        
        #user_following
        current_user_following = []
        c.execute('SELECT * FROM users WHERE email=?', (user_following,))
        returned_user_following = c.fetchone()

        if len(returned_user_following[3]) != 0:
            current_user_following = returned_user_following[3].split(',')

        current_user_following.append(user_to_follow)
        new_user_following = current_user_following.copy()
        new_user_following_str = ','.join(new_user_following)

        c.execute('UPDATE users SET following=? WHERE email=?', (new_user_following_str, user_following))
        conn.commit()


        #user_to_follow
        current_user_to_follow_followers = []
        current_user_to_follow_followers_n = 0

        c.execute('SELECT * FROM users WHERE email=?', (user_to_follow,))
        returned_user_to_follow = c.fetchone()

        if len(returned_user_to_follow[4]) != 0:
            current_user_to_follow_followers = returned_user_to_follow[4].split(',')
        current_user_to_follow_followers_n = int(returned_user_to_follow[5])

        current_user_to_follow_followers.append(user_following)
        new_user_to_follow_followers = current_user_to_follow_followers.copy()
        new_user_to_follow_followers_str = ','.join(new_user_to_follow_followers)

        current_user_to_follow_followers_n += 1
        current_user_to_follow_followers_n_str = str(current_user_to_follow_followers_n)

        c.execute('UPDATE users SET followers=?, followers_n=? WHERE email=?', (new_user_to_follow_followers_str, current_user_to_follow_followers_n_str, user_to_follow))
        conn.commit()

def unfollow_user(user_following:str, user_to_follow:str):
    with conn:
        c = conn.cursor()

        if is_following_user(user_following, user_to_follow) == False:
            return "User allready not following"
        
        #user_following
        current_user_following = []
        c.execute('SELECT * FROM users WHERE email=?', (user_following,))
        returned_user_following = c.fetchone()

        if len(returned_user_following[3]) != 0:
            current_user_following = returned_user_following[3].split(',')

        current_user_following.remove(user_to_follow)
        new_user_following = current_user_following.copy()
        new_user_following_str = ','.join(new_user_following)

        c.execute('UPDATE users SET following=? WHERE email=?', (new_user_following_str, user_following))
        conn.commit()


        #user_to_follow
        current_user_to_follow_followers = []
        current_user_to_follow_followers_n = 0

        c.execute('SELECT * FROM users WHERE email=?', (user_to_follow,))
        returned_user_to_follow = c.fetchone()

        if len(returned_user_to_follow[4]) != 0:
            current_user_to_follow_followers = returned_user_to_follow[4].split(',')
        current_user_to_follow_followers_n = int(returned_user_to_follow[5])

        current_user_to_follow_followers.remove(user_following)
        new_user_to_follow_followers = current_user_to_follow_followers.copy()
        new_user_to_follow_followers_str = ','.join(new_user_to_follow_followers)

        current_user_to_follow_followers_n -= 1
        current_user_to_follow_followers_n_str = str(current_user_to_follow_followers_n)

        c.execute('UPDATE users SET followers=?, followers_n=? WHERE email=?', (new_user_to_follow_followers_str, current_user_to_follow_followers_n_str, user_to_follow))
        conn.commit()

def get_folowers_n(user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (user,))
        return c.fetchone()[5]

def get_users_following(user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (user,))
        returned_user = c.fetchone()

        user_following_str = returned_user[3]
        if user_following_str == '':
            return []
        
        return user_following_str.split(',')

def get_users_following_users_following(user:str):
    users_friends_friends = []
    for users_following in get_users_following(user):
        for users_users_following in get_users_following(users_following):
            if users_users_following != user:
                users_friends_friends.append(users_users_following)
    
    return users_friends_friends  

def add_user_interest(user:str, interest:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM interests WHERE user=?', (user,))
        raw = c.fetchone()
        if raw == ():
            current_intersets = []
        else:
            current_intersets = str(raw[1]).split(",")

        new_interests = []
        new_interests += current_intersets

        if current_intersets == []:
            new_interests = [interest]
        else:
            if interest not in current_intersets:
                new_interests.append(interest)

        try:
            new_interests.remove("")
        except:
            pass
        new_interests = ",".join(new_interests)

        c.execute('UPDATE interests SET interests=? WHERE user=?', (new_interests, user))
        conn.commit()

def get_user_interests(user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM interests WHERE user=?', (user,))
        raw = c.fetchone()
        if raw == None:
            intersets = []
        else:
            intersets = str(raw[1]).split(",")

        return intersets

def change_password(user:str, new_password:str):
    with conn:
        c = conn.cursor()
        c.execute('UPDATE users SET password=? WHERE email=?', (new_password, user))
        conn.commit()

#Posts
def new_post(user:str, content:str):
    if content == "" or content == " "*len(content):
        return "empty post"
    with conn:
        c = conn.cursor()
        thetime = time.time()
        thetime = str(thetime)
        post_id = generate_id("posts", "id")
        post_genre = alg.get_post_genre(str(content))
        c.execute('INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?)', (user, content, "0", "", post_id, thetime))
        c.execute('INSERT INTO postgenre VALUES(?, ?)', (post_id, post_genre))
        conn.commit()
    return "success"

def delete_post(post_id:str):
    add_post_to_deleted(post_id)

    with conn:
        c = conn.cursor()
        c.execute("DELETE FROM posts WHERE id=?", (post_id,))
        c.execute("DELETE FROM postgenre WHERE postid=?", (post_id,))
        conn.commit()

def add_post_to_deleted(post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
        post = c.fetchone()

        c.execute("INSERT OR IGNORE INTO deletedposts VALUES(?, ?, ?, ?, ?, ?)", (post[0], post[1], post[2], post[3], post[4], post[5]))
        conn.commit()
        return "success"

def get_posts(user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts')
        posts = c.fetchall()
        posts_return = []
        for post in posts:
            if user_liked_post(user, post[4]):
                posts_return.append(post+(True,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))
            else:
                posts_return.append(post+(False,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))
        return posts_return

def get_posts_by_user(user:str, current_user:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts WHERE user=?', (user,))
        posts = c.fetchall()

        posts_return = []

        total_likes = 0
        total_posts = 0

        for post in posts:
            total_posts += 1
            total_likes += int(post[2])
            if user_liked_post(current_user, post[4]):
                posts_return.append(post+(True,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))
            else:
                posts_return.append(post+(False,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))

        return [posts_return, total_likes, total_posts]

def get_post_by_post_id(user:str, post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
        post = c.fetchone()
        post_return = ()
        if user_liked_post(user, post[4]):
            post_return = (post+(True,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))
        else:
            post_return = (post+(False,get_comments_by_parrent_post(post[4])[::-1], get_users_id_by_username(post[0]), str(len(get_comments_by_parrent_post(post[4])))))
        return post_return

def get_post_genre(post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM postgenre WHERE postid=?', (post_id,))
        return c.fetchone()[1]

def get_latest_posts(user:str, n:int):
    with conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM posts")
        response = c.fetchall()

        if len(response) > n:
            response = response[len(response)-n:]

        to_output = []

        for post in response:
            to_output.append(get_post_by_post_id(user, post[4]))

        return to_output

def get_latest_posts_by_genre(user:str, n:int, genre:str):
    with conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM postgenre WHERE genre=?", (genre,))
        response = c.fetchall()

        if len(response) > n:
            response = response[len(response)-n:]

        to_output = []

        for post in response:
            to_output.append(get_post_by_post_id(user, post[0]))

        return to_output

def like_post(user:str, post_id:str):
    with conn:
        c = conn.cursor()
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
    with conn:
        c = conn.cursor()
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
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
        post = c.fetchone()

        post_user_likes = str(post[3]).split(',')

        return True if user in post_user_likes else False

def read_post(user:str, post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM readposts WHERE user=? AND post=?', (user, post_id))
        if c.fetchall() != []:
            return "Allready read"
        c.execute('INSERT INTO readposts VALUES(?, ?)', (user, post_id))
        conn.commit()

def is_post_read(user:str, post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM readposts WHERE user=? AND post=?', (user, post_id))
        if c.fetchall() == []:
            return False
        return True

#Comments
def new_comment(user:str, content:str, parrent_post_id:str):
    if content == "" or content == " "*len(content):
        return "empty comment"
    with conn:
        c = conn.cursor()
        c.execute('INSERT INTO comments VALUES(?, ?, ?, ?, ?)', (user, content, parrent_post_id, generate_id("comments", "id"), get_users_id_by_username(user)))
        conn.commit()
    return "success"

def get_comments_by_parrent_post(parrent_post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM comments WHERE parrent_id=?', (parrent_post_id,))
        return c.fetchall()