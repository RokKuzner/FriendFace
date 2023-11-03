import database as db
import time
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

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

#Genre prediction
custom_objects = {"KerasLayer": hub.KerasLayer}

model = tf.keras.models.load_model('AI_models/genre_prediction/models/genre_prediction.h5', custom_objects=custom_objects)

df = pd.read_csv("AI_models/genre_prediction/data/data.csv", usecols=["genre", "description"])
df = df.dropna(subset=["genre", "description"])
label_encoder = LabelEncoder()
label_encoder.fit_transform(df["genre"])

def get_post_genre(post_content:str):
    #Cleaning up data
    content_modifyed = ""
    for char in post_content:
        if char.isalpha() == True or char == " " or char.isnumeric():
            content_modifyed += char
    while len(content_modifyed) != 0 and content_modifyed[0] == " ":
        content_modifyed = content_modifyed[1:]
    while len(content_modifyed) != 0 and content_modifyed[-1] == " ":
        content_modifyed = content_modifyed[:len(content_modifyed)-1]
    post_content = content_modifyed

    content = [post_content]
    content = np.array(content)
    content = tf.convert_to_tensor(content, dtype=tf.string)

    predictions = model(content)

    predicted_labels = label_encoder.inverse_transform(predictions.numpy().argmax(axis=1))

    return predicted_labels[0]