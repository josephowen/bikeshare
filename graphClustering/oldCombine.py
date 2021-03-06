import json
import sys

if len(sys.argv) == 5:
    inputFile = sys.argv[1]
    stationsFile = sys.argv[2]
    outputFile = sys.argv[3]
    colorFile = sys.argv[4]
else:
    inputFile = "../data/nyc/dtwClustering/weekdays/dendrogramGroups100.json"
    stationsFile = "../data/nyc/stations.json"
    outputFile = "../data/nyc/dtwClustering/stationsGroupedWeekdays100.json"
    colorFile = "../data/nyc/dtwClustering/weekdays/colors100.json"

with open(inputFile, "r") as f:
    groups = json.load(f)
    
with open(stationsFile, "r") as f:
    stations = json.load(f)
    
with open(colorFile, "r") as f:
    colors = json.load(f)
    
stationLookup = {}

for i, station in enumerate(stations):
    stationLookup[int(station["id"])] = i
    
for i, group in enumerate(groups):
    for id in group["contents"]:
        if id in stationLookup:
            stations[stationLookup[id]]["group"] = i
            stations[stationLookup[id]]["color"] = colors[i]
        
with open(outputFile, "w") as f:
    json.dump(stations, f)