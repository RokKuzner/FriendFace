import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, LabelBinarizer

custom_objects = {"KerasLayer": hub.KerasLayer}

model = tf.keras.models.load_model('models/genre_prediction.h5', custom_objects=custom_objects)

descriptions = ["there is a new galery where you can paint pictures down in now york"]

descriptions = np.array(descriptions)
descriptions = tf.convert_to_tensor(descriptions, dtype=tf.string)

predictions = model(descriptions)

df = pd.read_csv("data/data.csv", usecols=["genre", "description"])
df = df.dropna(subset=["genre", "description"])
label_encoder = LabelEncoder()
label_encoder.fit_transform(df["genre"])

predicted_labels = label_encoder.inverse_transform(predictions.numpy().argmax(axis=1))

print(f"Predicted Genre: {predicted_labels[0]}")