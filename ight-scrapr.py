import requests
import json
import pandas as pd
import numpy as np

print("\033[1m" + "\nReading hashtag list from input file (hashtags.txt)..." + "\033[0m")
inputFile = open("hashtags.txt", mode="r")
input = inputFile.read()
inputFile.close()
inputList = input.split("\n")

print("\033[1m" + "Creating output CSV file (output.csv)..." + "\033[0m")
outputFile = open("output.csv", mode="w")
outputFile.write("Hashtag,# of Posts,Min Likes (Top),Mean Likes (Top),Median Time Between Posts (s) (Recent),% Video (Recent)\n")

print("\n---------")
for hashtag in inputList:
    if hashtag != "":
        print("\033[1m" + "Scraping/analyzing posts for " + hashtag + "..." + "\033[0m")
        page = requests.get("https://www.instagram.com/explore/tags/" + hashtag[1:])

        try:
            posts = json.loads(page.text[page.text.find("window._sharedData") + 21: page.text.find("};</script>") + 1])
        except json.JSONDecodeError:
            print("\033[91m" + u"\U0001F625" + " " + "There was an error getting posts for this hashtag " + u"\U0001F625" + "\033[0m")
            continue

        postCount = posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
        minTopLikes = 0
        meanTopLikes = 0
        medianRecentTime = 0
        percentRecentVids = 0

        if postCount != 0:
            i = 0
            totalTop = 0
            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]:
                if post["node"]["edge_liked_by"]["count"] < minTopLikes or i == 0:
                    minTopLikes = post["node"]["edge_liked_by"]["count"]
                totalTop += post["node"]["edge_liked_by"]["count"]
                i += 1
            meanTopLikes = totalTop / i
            print("Looked at " + str(i) + " top posts...")

            j = 0
            totalTimeList = []
            totalRecentVids = 0
            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                totalTimeList.append(post["node"]["taken_at_timestamp"])
                if post["node"]["is_video"]:
                    totalRecentVids += 1

                j += 1
                if j == 100:
                    break
            if j != 1:
                medianRecentTime = np.median(np.diff(sorted(totalTimeList)))
            percentRecentVids = (totalRecentVids / j) * 100
            print("Looked at " + str(j) + " recent posts...")
        else:
            print("\033[93m" + "No posts exist for this hashtag" + "\033[0m")

        outputFile.write(hashtag + "," + str(postCount) + "," + str(minTopLikes) + "," + str(meanTopLikes) + "," + str(medianRecentTime) + "," + str(percentRecentVids) + "\n")

outputFile.close()

print("\033[1m" + "----------\n\nConverting CSV data into a JSON file (output.json)..." + "\033[0m")
jsonOutputFile = open("output.json", "w")
jsonOutputFile.write(json.dumps(json.loads(pd.read_csv(r"output.csv").to_json()), indent=2))
jsonOutputFile.close()

print("\033[92m" + "\n" + u"\U0001F49A" + " Completed! " + u"\U0001F49A" + "\n" + "\033[0m")
