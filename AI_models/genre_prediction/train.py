import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import LabelEncoder, LabelBinarizer

#Loading dataset
df = pd.read_csv("data/data.csv", usecols=["genre", "description"])

#Data preperation
df = df.dropna(subset=["genre", "description"])

genres = df["genre"].unique()

label_encoder = LabelEncoder()
label_binarizer = LabelBinarizer()

df["genre"] = label_encoder.fit_transform(df["genre"])

train, val, test = np.split(df.sample(frac=1), [int(0.90*len(df)), int(0.95*len(df))])

def df_to_dataset(dataframe, shuffle=True, batch_size=512):
  df = dataframe.copy()
  labels = df.pop('genre')
  descriptions = df.pop("description")
  ds = tf.data.Dataset.from_tensor_slices((descriptions, labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  ds = ds.prefetch(tf.data.AUTOTUNE)
  return ds

train_data = df_to_dataset(train)
valid_data = df_to_dataset(val)
test_data = df_to_dataset(test)

#Making the model
hub_layer = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", dtype=tf.string, trainable=True)

model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(16, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)))
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(len(genres), activation="softmax"))

#Compiling the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
)

#Prepairing the model for training
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # Use validation loss for monitoring
    patience=3,          # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True  # Restore the best model weights
)

history = model.fit(train_data, epochs=15, validation_data=valid_data, callbacks=[early_stopping])

print("Evaluation:", model.evaluate(test_data))

model.save("models/genre_prediction.h5")