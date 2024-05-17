import sqlite3, random, string, time
import algorythms as alg
import keywordextractor
from datetime import datetime, timezone
import encryption

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

def relative_time(timestamp):
  """
  Calculates relative time string from a timestamp in seconds (assumed to be UTC).

  Returns:
    Relative time string (e.g., "3 hours ago", "4 years ago").
  """
  utc_timestamp = float(get_utc_timestamp())

  delta = utc_timestamp - timestamp

  seconds = delta
  minutes = seconds / 60
  hours = minutes / 60
  days = hours / 24
  months = days / 30
  years = months / 12

  if seconds < 1:
    return "just now"
  elif minutes < 1:
    if int(seconds) == 1:
        return "1 second ago"
    return f"{int(seconds)} seconds ago"
  elif hours < 1:
    if int(minutes) == 1:
        return "1 minute ago"
    return f"{int(minutes)} minutes ago"
  elif days < 1:
    if int(hours) == 1:
        return "1 hour ago"
    return f"{int(hours)} hours ago"
  elif months < 1:
    if int(days) == 1:
        return "1 day ago"
    return f"{int(days)} days ago"
  elif years < 1:
    if int(months) == 1:
        return "1 month ago"
    return f"{int(months)} months ago"
  else:
    if int(years) == 1:
        return "1 year ago"
    return f"{int(years)} years ago"

def get_utc_timestamp():
    current_time_utc = datetime.now(timezone.utc)
    utc_timestamp = current_time_utc.timestamp()
    return str(utc_timestamp)

#Users
def validate_user(username:str, password:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?',(username,))
        data = c.fetchone()

        if data is None:
            return False

        correct_password = encryption.decrypt(data[2])
        return password == correct_password

def add_user(username:str, password:str):
    with conn:
        c = conn.cursor()
        user_id = generate_id('users', 'id')
        c.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)', (username, user_id, encryption.encrypt(password), '', '', '0'))
        c.execute('INSERT INTO interests VALUES(?, ?)', (username, ""))
        conn.commit()
        return user_id

def get_users_id_by_username(username:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (username,))
        data = c.fetchone()

        return data[1] if data != None else None

def get_username_by_user_id(user_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT email FROM users WHERE id=?', (user_id,))
        return c.fetchone()[0]

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
        c.execute('UPDATE users SET password=? WHERE email=?', (encryption.encrypt(new_password), user))
        conn.commit()

#Posts
def new_post(user:str, content:str):
    if content == "" or content == " "*len(content):
        return "empty post"
    with conn:
        c = conn.cursor()

        utc_timestamp = get_utc_timestamp()

        post_id = generate_id("posts", "id")
        post_genre = alg.get_post_genre(str(content))

        keywords = keywordextractor.extract_keywords(content)
        keywords_lower_case = [keyword.lower() for keyword in keywords]
        joined_keywords = ",".join(keywords_lower_case)

        c.execute('INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?, ?)', (user, content, "0", "", post_id, utc_timestamp, joined_keywords))
        c.execute('INSERT INTO postgenre VALUES(?, ?)', (post_id, post_genre))
        add_post_to_keyword(post_id, keywords_lower_case)

        conn.commit()
    return "success"

def delete_post(post_id:str):
    add_post_to_deleted(post_id)

    for keyword in get_post_keywords(post_id):
        remove_post_from_keyword(post_id, keyword)

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
            posts_return.append(get_post_by_post_id(user, post[4]))
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
            posts_return.append(get_post_by_post_id(current_user, post[4]))

        return [posts_return, total_likes, total_posts]

def get_post_by_post_id(user:str, post_id:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM posts WHERE id=?', (post_id,))
        post = c.fetchone()
        post_return = ()

        post_return = {"author_username":post[0],
                       "content":post[1],
                       "likes":post[2],
                       "users_liked":post[3],
                       "id":post[4],
                       "time":post[5],
                       "comments":get_comments_by_parrent_post(post[4]),
                       "author_id":get_users_id_by_username(post[0]),
                       "commentsN":str(len(get_comments_by_parrent_post(post[4]))),
                       "timePretty": relative_time(float(post[5])),
                       "keywords":post[6].split(",")}

        post_return["liked"] = True if user_liked_post(user, post_return["id"]) else False

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

def get_post_keywords(post_id:str) -> list[str]:
    with conn:
        c = conn.cursor()
        c.execute('SELECT keywords FROM posts WHERE id=?', (post_id,))
        response = c.fetchone()

        return response[0].split(",") if response!= None else []

def get_all_keywords():
    with conn:
        c = conn.cursor()
        c.execute('SELECT keyword FROM keywords')
        response = c.fetchall()

        keywords = [tuple[0] for tuple in response]
        return keywords

def get_posts_by_keyword(keyword:str) -> list[str]:
    with conn:
        c = conn.cursor()
        c.execute('SELECT posts FROM keywords WHERE keyword=?', (keyword,))
        response = c.fetchone()

        return response[0].split(",") if response!= None else []

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
    
#Search
def add_post_to_keyword(post_id:str, keywords:list[str]):
    for keyword in keywords:
        with conn:
            c = conn.cursor()
            c.execute('SELECT posts FROM keywords WHERE keyword=?', (keyword,))
            posts = c.fetchone()

            if posts == None:
                c.execute('INSERT INTO keywords VALUES(?,?)', (keyword, post_id))
            else:
                c.execute('UPDATE keywords SET posts=? WHERE keyword=?', (str(post_id+","+posts[0]), keyword))
                
            conn.commit()

def remove_post_from_keyword(post_id:str, keyword:str):
    with conn:
        c = conn.cursor()
        c.execute('SELECT posts FROM keywords WHERE keyword=?', (keyword,))
        posts = c.fetchone()

        if posts != None:
            posts = posts[0].split(",")
            posts.remove(post_id)
            c.execute('UPDATE keywords SET posts=? WHERE keyword=?', (",".join(posts), keyword))
            conn.commit()

#FriendChat
def dm_exists(user1_id:str, user2_id:str):
    with conn:
        c = conn.cursor()

        c.execute("SELECT * FROM chat_dms WHERE user1=? AND user2=?", (user1_id, user2_id))
        return_1 = c.fetchone()
        c.execute("SELECT * FROM chat_dms WHERE user1=? AND user2=?", (user2_id, user1_id))
        return_2 = c.fetchone()

        if return_1 != None or return_2 != None:
            return True
        return False

def create_dm(user_creating_id:str, user_participating_id:str):
    if dm_exists(user_creating_id, user_participating_id):
        return "DM allready exists"
    if user_creating_id == user_participating_id:
        return "Can't create dm with yourself"

    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO chat_dms VALUES(?, ?, ?, ?)", (user_creating_id, user_participating_id, generate_id("chat_dms", "dm_id"), get_utc_timestamp()))
        conn.commit()

def get_dm_members(dm_id:str):
    with conn:
        c = conn.cursor()
        c.execute("SELECT user1, user2 FROM chat_dms WHERE dm_id=?", (dm_id,))
        return list(c.fetchone())
    
def new_message(dm_id:str, sender_id:str, content:str):
    if sender_id not in get_dm_members(dm_id):
        return "User not in dm"
    
    utc_timestamp = get_utc_timestamp()

    encrypted_content = encryption.encrypt(content)

    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO chat_msgs VALUES(?, ?, ?, ?, ?)", (dm_id, generate_id("chat_msgs", "message_id"), sender_id, utc_timestamp, encrypted_content))
        c.execute('UPDATE chat_dms SET last_activity=? WHERE dm_id=?', (utc_timestamp, dm_id))
        conn.commit()

def get_dm_messages(dm_id:str):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chat_msgs WHERE dm_id=?", (dm_id,))
        messages = c.fetchall()

    messages_to_return = []

    for message in messages:
        messages_to_return.append(
            {
                "dm_id": message[0],
                "message_id": message[1],
                "sender_id": message[2],
                "sender_username": get_username_by_user_id(message[2]),
                "timestamp": float(message[3]),
                "time_pretty": relative_time(float(message[3])),
                "content": encryption.decrypt(message[4])
            }
        )

    return messages_to_return

def get_users_dms(user_id:str):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chat_dms WHERE user1=? OR user2=?", (user_id, user_id))
        return c.fetchall()
    
def get_all_users_dm_companions(user_id:str):
    output = []
    dms = get_users_dms(user_id)

    for dm in dms:
        if dm[0] == user_id:
            output.append((dm[1], get_username_by_user_id(dm[1]), dm[2]))
        else:
            output.append((dm[0], get_username_by_user_id(dm[0]), dm[2]))

    return output

def get_latest_active_dms_by_user(user_id:str):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chat_dms WHERE user1=? OR user2=? ORDER BY last_activity DESC", (user_id, user_id))
        return c.fetchall()
    
def get_dm_coresponder(dm_id:str, user_id:str):
    with conn:
        c = conn.cursor()
        c.execute("SELECT user1, user2 FROM chat_dms WHERE dm_id=?", (dm_id,))
        dm = c.fetchone()

        if dm[0] == user_id:
            return dm[1]
        else:
            return dm[0]

def get_latest_dm_message(dm_id:str, current_user_id:str):
    dm_messages =  get_dm_messages(dm_id)

    if dm_messages != []:
        return dm_messages[-1]
    else:
        coresponder_id = get_dm_coresponder(dm_id, current_user_id)
        return {
                "dm_id": dm_id,
                "message_id": None,
                "content": "You have no messages in this dm.",
                "sender_id": coresponder_id,
                "sender_username": get_username_by_user_id(coresponder_id),
                "coresponder_id": coresponder_id,
                "coresponder_username": get_username_by_user_id(coresponder_id)
            }