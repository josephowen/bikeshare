import matplotlib.pyplot as plt
from datetime import datetime
import json
from random import random
import sys
from time import sleep
import colorsys as cs

with open(sys.argv[1], "r") as f:
    allStations = json.load(f)

for station in allStations:
    x, y = [], []
    for thisTime in station["times"]:
        x.append(datetime(2000, 1, 1, int(thisTime["hour"]), int(thisTime["minute"])))
        y.append(thisTime["percentFull"]*100)
    
    H = 240.0/360
    S = 0.5 + random()*0.5
    V = 0.7 + random()*0.3
    
    thisColor = cs.hsv_to_rgb(H, S, V)
    
    plt.plot_date(x, y, marker=',', linestyle='-', color=thisColor)

title = []
for i in range(2, len(sys.argv)):
    title.append(sys.argv[i])
title = " ".join(title)
plt.title(title)
plt.xlabel("Time")
plt.ylabel("Percent Full")
# plt.title(sys.argv[1])
plt.show()