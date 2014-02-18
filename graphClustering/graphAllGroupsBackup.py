import matplotlib.pyplot as plt
from datetime import datetime
import json
from random import random
import sys
from time import sleep

with open("colors.dat", "r") as f:
    allColors = json.load(f)

with open(sys.argv[1], "r") as f:
    allGroups = json.load(f)

for i, group in enumerate(allGroups):
    # if len(group["contents"]) < 10:
        # continue
    y = group["times"]
    x = range(len(y))
    plt.plot(x, y, marker=',', linestyle='-', color=(random(), random(), random()))

plt.xlabel("Minute")
plt.ylabel("% Full")
plt.title(sys.argv[1])
plt.show()