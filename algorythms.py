import database as db
import time
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import translate

def get_personalized_posts(user:str):
    #Create a dict for graded posts
    graded_posts = {}

    #Grade every post on platform
    for post in db.get_posts(user):
        grade = grade_post(user, post)

        #If key allready exists
        while grade in graded_posts:
            grade += 0.000001

        #Add garaded post with grade as key to dict
        graded_posts[grade] = post


    #Sort dict keys
    sorted_keys = list(graded_posts)
    sorted_keys.sort()

    #Return sorted values
    to_return = []
    for key in sorted_keys:
        to_return.append(graded_posts[key])

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

    total_points += scale_to_range(time_posted, 0, current_time)

    if db.get_post_genre(post[4]) in db.get_user_interests(user):
        total_points += 15

    if db.is_post_read(user, post[4]) == True:
        total_points = total_points / 4

    return total_points

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def scale_to_range(value, x, y):
    # Calculate the normalized value within the range [x, y]
    normalized_value = (value - x) / (y - x)

    # Scale the normalized value to the range [0, 10]
    scaled_value = normalized_value * 10

    return scaled_value

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
    post_content = content_modifyed.lower()

    #Translate content to english (only for prediction)
    language = translate.detect_lang(post_content)
    if language != "en":
        post_content = translate.translate(post_content, language)

    #Prediction
    content = [post_content]
    content = np.array(content)
    content = tf.convert_to_tensor(content, dtype=tf.string)

    predictions = model(content)

    predicted_labels = label_encoder.inverse_transform(predictions.numpy().argmax(axis=1))

    return predicted_labels[0]