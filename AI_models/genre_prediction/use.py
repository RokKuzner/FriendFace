import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np

#Loading dataset and unique varietyes
df = pd.read_csv("data/data.csv", usecols=["genre", "description"])
df = df.dropna(subset=["genre", "description"]) #Drops all empty rows
genres = df["genre"].unique()

#Create custom objects
custom_objects = {
    "KerasLayer": hub.KerasLayer
}

# Load the model with the custom object dictionary
model = tf.keras.models.load_model('models/genre_prediction.h5', custom_objects=custom_objects)

to_predict = ["surveillance technology like stingray can sweep up data from any cell phone in its range"]

predictions = model.predict(to_predict)

predicted_class_index = np.argmax(predictions)
predicted_class = genres[predicted_class_index]

print("Predicted class:", predicted_class)