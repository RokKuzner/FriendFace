import pandas as pd
import csv
import json

#Joined list of data
data = []

#Data from nyt articles
df = pd.read_csv("data/nyt-articles-2020.csv", usecols=["newsdesk", "abstract"])

df = df.dropna(subset=["newsdesk", "abstract"])

genres = df["newsdesk"].unique()
use = ["games", "science", "culture", "sports", "travel", "politics", "business", "technology", "movies"]

for index, row in df.iterrows():
    new_value = ""
    newdesk_value = df.at[index, "newsdesk"]
    if str(newdesk_value).lower() in use:
        new_value = str(newdesk_value).lower()
    else:
        new_value = "other"

    description = str(df.at[index, "abstract"].lower()).replace('"', "")
    
    if description == "" or description == str(" "*len(description)):
        continue

    data.append((description, str(new_value).lower()))

#data from others
with open('data/News_Category_Dataset_v3.json', 'r', encoding="utf-8") as f:
  json_data = json.load(f)

categoryes_replace = {"tech":"technology", "science":"science", "arts & culture":"culture", "business":"business", "politics":"politics", "entertainment":"entertainment", "sports":"sports"}

for i in json_data:
    description = str(i["short_description"].lower()).replace('"', "")
    if description == "" or description == str(" "*len(description)):
        continue
    if i["category"].lower() in list(categoryes_replace.keys()):
        data.append((description, str(categoryes_replace[i["category"].lower()])))
    else:
        data.append((description, "other"))


#Oversampling data
categoryes = {}
for i in data:
    if i[1] in categoryes:
        categoryes[i[1]].append(i)
    else:
        categoryes[i[1]] = [i]

max_category_n = 0
max_category_key = ''
for i in categoryes:
    if len(categoryes[i]) > max_category_n:
        max_category_n = len(categoryes[i])
        max_category_key = i

for i in data:
    if i[1] != max_category_key:
        multipication = int(max_category_n/len(categoryes[i[1]]))
        max_multiplication = 200
        if multipication > max_multiplication:
            multipication = max_multiplication
        categoryes[i[1]] = categoryes[i[1]]*multipication

data = []
for i in categoryes:
    for indx in categoryes[i]:
        data.append(indx)

#Make a brand new and clean and shiny csv file
with open("data/data.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['description', 'genre'])

    for index, row in enumerate(data):
        #data[index][0][0] = '"' + str(data[index][0][0]).replace('"', "") + '"'
        writer.writerow([data[index][0], data[index][1]])

'''
with open('data/News_Category_Dataset_v3.json', "r", encoding="utf-8") as json_file:
    json_data = json_file.read()
    json_list = json_data.split("\n")
    json_list_joined = ",\n".join(json_list)

with open('data/News_Category_Dataset_v3.json', "w") as json_file:
    json_file.write(json_list_joined)
'''