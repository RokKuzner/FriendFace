import database as db

def get_personalized_posts(user:str):
    user_following = db.get_users_following(user_following)

    if user_following == []:
        return db.get_posts(user)
    
    to_return = []

def grade_post(user:str, user_following:list, post):
    pass