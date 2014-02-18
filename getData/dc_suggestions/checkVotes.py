#!/usr/bin/python

import json
import sys

with open(sys.argv[1], "r") as f:
    data = json.load(f)

likes = 0
dislikes = 0
neither = 0

numToPrint = 0

for station in data:
    for comment in station["comments"]:
        which = comment["vote"]
        if which == "likes":
            likes += 1
        elif which == "dislikes":
            dislikes += 1
        else:
            neither += 1
            print station["LocNumber"]
            if numToPrint > 0:
                print comment
                numToPrint -= 1

print likes, "likes"
print dislikes, "dislikes"
print neither, "blank"
