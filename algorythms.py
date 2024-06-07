import database as db
import time
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import translate

def get_personalized_posts(user:str):
    #posts to grade
    posts_to_grade = []

    #Last 10000 posts
    latest_posts = db.get_latest_posts(user, 10000)
    first_latest_post = latest_posts[0]
    
    posts_to_grade += latest_posts

    #posts from all the users subscribed to
    users_following = db.get_users_following(user)
    users_following_posts = []
    for user_following in users_following:
        users_following_posts += db.get_posts_by_user(user_following, user)[0]

    for post in users_following_posts:
        if float(post["time"]) < float(first_latest_post["time"]): #if the post isn't already one of the latest 10000 posts
            posts_to_grade.append(post)

    #Latest 200 posts with user's interests
    for interest in db.get_user_interests(user):
        posts_with_interest = db.get_latest_posts_by_genre(user, 200, interest)

        for post in posts_with_interest:
            if (post["author_username"] not in users_following) and (float(post["time"]) < float(first_latest_post["time"])): #if the post isn't posted my a user that is followed or already one of the latest 10000 posts
                posts_to_grade.append(post)

    #Create a dict for graded posts
    graded_posts_by_grade = {}

    #Grade posts
    for post in posts_to_grade:
        grade = grade_post(user, post)

        #If key allready exists
        while grade in graded_posts_by_grade:
            grade += 0.000001

        #Add garaded post with grade as key to dict
        graded_posts_by_grade[grade] = post


    #Sort dict keys
    sorted_grades = sorted(graded_posts_by_grade)

    #Return sorted values
    sorted_graded_posts = [graded_posts_by_grade[key] for key in sorted_grades]

    return sorted_graded_posts

def grade_post(user:str, post):
    total_points = 0
    current_time = time.time()

    time_posted = float(post["time"])
    users_following_users_following = db.get_users_following_users_following(user) #this are the users that are followed by users that the user follows

    if db.is_following_user(user, post["author_username"]):
        total_points += 10
    if post["author_username"] in users_following_users_following:
        total_points += 3

    total_points += scale_to_range(time_posted, 0, current_time, 10)

    if db.get_post_genre(post["id"]) in db.get_user_interests(user):
        total_points += 15

    if db.is_post_read(user, post["id"]) == True:
        total_points = total_points / 4

    return total_points

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def scale_to_range(value, x_original_scale, y_original_scale, new_scale_max):
    # Calculate the normalized value within the range [x_original_scale, y_original_scale]
    normalized_value = (value - x_original_scale) / (y_original_scale - x_original_scale)

    # Scale the normalized value to the range [0, new_scale_max]
    scaled_value = normalized_value * new_scale_max

    return scaled_value

#Genre prediction
custom_objects = {"KerasLayer": hub.KerasLayer}

model = tf.keras.models.load_model('AI_models/genre_prediction/models/genre_prediction.h5', custom_objects=custom_objects)

df = pd.read_csv("AI_models/genre_prediction/data/data.csv", usecols=["genre", "description"])
df = df.dropna(subset=["genre", "description"])
label_encoder = LabelEncoder()
label_encoder.fit_transform(df["genre"])

def get_post_genre(post_content:str):
    #Clean up data
    post_content = "".join(filter(lambda char: char.isalpha() or char.isnumeric() or char == " ", post_content)).strip().lower()

    #Translate content to english (only for prediction)
    all_not_alphaa = True

    for char in post_content:
        if char.isalpha():
            all_not_alphaa = False
            exit

    if all_not_alphaa == False:
        language = translate.detect_lang(post_content)
        if language != "en":
            post_content = translate.translate(post_content, language)

            if post_content == {"status": "error"}:
                return "other"

    #Prediction
    content = [post_content]
    content = np.array(content)
    content = tf.convert_to_tensor(content, dtype=tf.string)

    predictions = model(content)

    predicted_labels = label_encoder.inverse_transform(predictions.numpy().argmax(axis=1))

    return predicted_labels[0]