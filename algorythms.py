import database as db
import time

def get_personalized_posts(user:str):
    user_following = db.get_users_following(user)
    posts_with_grade = {}

    for post in db.get_posts(user):
        grade = grade_post(user, post)
        posts_with_grade[grade] = post


    sorted_keys = list(posts_with_grade)
    sorted_keys.sort()
    to_return = []
    for key in sorted_keys:
        to_return.append(posts_with_grade[key])

    return to_return

def grade_post(user:str, post):
    total_points = 0
    current_time = time.time()
    time_posted = float(post[5])
    users_following_users_following = db.get_users_following_users_following(user)

    if db.is_following_user(user, post[0]):
        total_points += 15
    elif post[0] in users_following_users_following:
        total_points += 5

    total_points += (time_posted) / (current_time/5)

    return total_points

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip