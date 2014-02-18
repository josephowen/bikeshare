import colorsys as cs
from random import random
import json

numColors = 7

colors = []

for i in range(numColors):
    H = (float(i)/numColors*360)/360
    S = 0.9 + random()*0.1
    V = 0.7 + random()*0.3
    
    thisColor = cs.hsv_to_rgb(H, S, V)
    thisColorJson = {}
    thisColorJson["r"] = thisColor[0]
    thisColorJson["g"] = thisColor[1]
    thisColorJson["b"] = thisColor[2]
    colors.append(thisColorJson)

    
with open("colors.dat", "w") as f:
    json.dump(colors, f)