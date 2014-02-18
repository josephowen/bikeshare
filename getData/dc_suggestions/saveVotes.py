#!/usr/bin/python

import json
import sys

with open(sys.argv[1], "r") as f:
    data = json.load(f)

for station in data:
    votes = 0
    for comment in station["comments"]:
        which = comment["vote"]
        if which == "likes" or which == "":
            votes += 1
        elif which == "dislikes":
            votes -= 1
    station["votes"] = votes

with open(sys.argv[1], "w") as f:
    json.dump(data, f)
