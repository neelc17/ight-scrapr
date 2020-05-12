import requests
import json
import pandas as pd

print("Reading hashtag list from hashtags.txt...")
inputFile = open("hashtags.txt", mode="r")
input = inputFile.read()
inputFile.close()
inputList = input.split("\n")

print("Creating output CSV file (output.csv)...")
outputFile = open("output.csv", mode="w")
outputFile.write("Hashtag,# of Posts,Min Top Post Likes,Mean Top Post Likes\n")

print("Scraping/analyzing data of top posts from the following hashtags:")
for hashtag in inputList:
    if hashtag != "":
        print(hashtag)
        URL = "https://www.instagram.com/explore/tags/" + hashtag[1:]
        page = requests.get(URL)

        posts = json.loads(page.text[page.text.find("window._sharedData") + 21: page.text.find("};</script>") + 1])

        postCount = posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
        meanTopPostLikes = 0
        minTopPostLikes = 0

        i = 0
        total = 0
        for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]:
            if post["node"]["edge_liked_by"]["count"] < minTopPostLikes or minTopPostLikes == 0:
                minTopPostLikes = post["node"]["edge_liked_by"]["count"]
            total += post["node"]["edge_liked_by"]["count"]
            i += 1
        if i != 0:
            meanTopPostLikes = total / i

        outputFile.write(hashtag + "," + str(postCount) + "," + str(minTopPostLikes) + "," + str(meanTopPostLikes) + "\n")

outputFile.close()

print("Converting CSV data into a JSON file (output.json)...")
jsonOutputFile = open("output.json", "w")
jsonOutputFile.write(json.dumps(json.loads(pd.read_csv(r"output.csv").to_json()), indent=2))
jsonOutputFile.close()

print("Completed!")
