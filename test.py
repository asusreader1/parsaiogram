import json

with open("news_dict.json") as file:
    news_dict = json.load(file)

search_id = "349505"

if search_id in news_dict:
    print("new already addded")
else:
    print("fresh newsss")
