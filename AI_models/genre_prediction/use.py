import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

custom_objects = {"KerasLayer": hub.KerasLayer}

model = tf.keras.models.load_model('models/genre_prediction.h5', custom_objects=custom_objects)

df = pd.read_csv("data/data.csv", usecols=["genre", "description"])
df = df.dropna(subset=["genre", "description"])
label_encoder = LabelEncoder()
label_encoder.fit_transform(df["genre"])

while True:
    user_input = input("Post: ")
    user_input = user_input.lower()
    if user_input == "quit":
        break

    description_modifyed = ""
    for char in user_input:
        if char.isalpha() == True or char == " " or char.isnumeric():
            description_modifyed += char
    if len(description_modifyed) != 0 and description_modifyed[0] == " ":
        description_modifyed = description_modifyed[1:]
    user_input = description_modifyed

    if len(user_input) < 15 or 0 or user_input == str(" "*len(user_input)) or user_input.isnumeric():
        print("Invalid input!")
        continue


    descriptions = [user_input]

    descriptions = np.array(descriptions)
    descriptions = tf.convert_to_tensor(descriptions, dtype=tf.string)

    predictions = model(descriptions)

    predicted_labels = label_encoder.inverse_transform(predictions.numpy().argmax(axis=1))

    print(f"Predicted Genre: {predicted_labels[0]}")