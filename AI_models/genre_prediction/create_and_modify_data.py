import pandas as pd
import csv

#Loading dataset
df = pd.read_csv("data/nyt-articles-2020.csv", usecols=["newsdesk", "abstract"])

#Data preperation
df = df.dropna(subset=["newsdesk", "abstract"])

genres = df["newsdesk"].unique()
use = ["games", "science", "culture", "sports", "travel", "politics", "business", "technology", "movies"]

with open("data/data.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['description', 'genre'])

    for index, row in df.iterrows():
        new_value = ""
        newdesk_value = df.at[index, "newsdesk"]
        if str(newdesk_value).lower() in use:
            new_value = str(newdesk_value).lower()
        else:
            new_value = "other"

        writer.writerow([str(df.at[index, "abstract"]).lower(), new_value])