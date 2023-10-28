import pandas as pd
import csv
import json

#Data from nyt articles
def get_data_from_nytarticles():
    d = []
    df = pd.read_csv("data/nyt-articles-2020.csv", usecols=["newsdesk", "headline"])

    df = df.dropna(subset=["newsdesk", "headline"])

    use = ["science", "culture", "sports", "travel", "politics", "business", "technology", "movies"]

    for index, row in df.iterrows():
        new_value = ""
        newdesk_value = df.at[index, "newsdesk"]
        if str(newdesk_value).lower() in use:
            new_value = str(newdesk_value).lower()
        else:
            new_value = "other"

        description = str(df.at[index, "headline"]).lower()
        data.append((description, str(new_value).lower()))

    return d

#data from others
def get_data_from_others():
    d = []
    with open('data/News_Category_Dataset_v3.json', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

    categoryes_replace = {"tech":"technology", "science":"science", "arts & culture":"culture", "business":"business", "politics":"politics", "entertainment":"entertainment", "sports":"sports"}

    for i in json_data:
        description = str(i["headline"]).lower()
        if i["category"].lower() in list(categoryes_replace.keys()):
            data.append((description, str(categoryes_replace[i["category"].lower()])))
        else:
            data.append((description, "other"))
        
    return d

#Data from science subreddit
def get_data_from_science_subreddit():
    d = []

    df = pd.read_csv("data/science.csv", usecols=["title", "body"])
    df = df.dropna(subset=["title", "body"])

    for index, row in df.iterrows():
        if df.at[index, "body"] == "":
            description = str(df.at[index, "title"]).lower()
        else:
            description = str(df.at[index, "body"]).lower()
        data.append((description, "science"))

    return d

#Data from techonology subreddit
def get_data_from_technology_subreddit():
    d = []
    df = pd.read_csv("data/technology.csv", usecols=["title"])
    df = df.dropna(subset=["title"])

    for index, row in df.iterrows():
        description = str(df.at[index, "title"]).lower()
        data.append((description, "technology"))

    return d

data = []
data += get_data_from_nytarticles()
data += get_data_from_others()
data += get_data_from_science_subreddit()
data += get_data_from_technology_subreddit()

#cleaning up the data
data_modyfied = []
for i in data:
    description = i[0]
    genre = i[1]

    description_modifyed = ""

    for char in description:
        if char.isalpha() == True or char == " " or char.isnumeric():
            description_modifyed += char

    while len(description_modifyed) != 0 and description_modifyed[0] == " ":
        description_modifyed = description_modifyed[1:]
    while len(description_modifyed) != 0 and description_modifyed[-1] == " ":
        description_modifyed = description_modifyed[:len(description_modifyed)-1]

    description = description_modifyed
    if len(description) < 20 or description == str(" "*len(description)) or description.isnumeric():
        pass
    else:
        data_modyfied.append((description, genre))
data = data_modyfied

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