import json
import sys

if len(sys.argv) == 4:
    inputFile = sys.argv[1]
    stationsFile = sys.argv[2]
    groupName = sys.argv[3]
    #colorFile = sys.argv[4]
else:
    print "Missing parameters"
    exit(0)

with open(inputFile, "r") as f:
    groups = json.load(f)
    
with open(stationsFile, "r") as f:
    stations = json.load(f)
    
#with open(colorFile, "r") as f:
#    colors = json.load(f)
    
stationLookup = {}

for i, station in enumerate(stations):
    stationLookup[int(station["id"])] = i
    
for i, group in enumerate(groups):
    for id in group["contents"]:
        if id in stationLookup:
            stations[stationLookup[id]][groupName] = i
            #stations[stationLookup[id]]["color"] = colors[i]
    
with open(stationsFile, "w") as f:
    json.dump(stations, f)
    
#with open(outputFile, "w") as f:
#    json.dump(stations, f)