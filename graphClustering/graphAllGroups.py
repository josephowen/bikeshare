import matplotlib.pyplot as plt
from datetime import datetime
import json
from random import random
import sys
from time import sleep

with open("colors.dat", "r") as f:
    allColors = json.load(f)

with open("../data/nyc/dtwClustering/"+sys.argv[1], "r") as f:
    allGroups = json.load(f)

for i, group in enumerate(allGroups):
    # if len(group["contents"]) < 10:
        # continue
    y = group["times"]
    x = range(len(y))
    thisColor = allColors[i]
    plt.plot(x, y, marker=',', linestyle='-', color=(thisColor["r"], thisColor["g"], thisColor["b"]))

plt.xlabel("Minute")
plt.ylabel("% Full")
plt.title(sys.argv[1])
plt.show()