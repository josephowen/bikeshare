import json
import sys

if len(sys.argv) == 3:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
else:
    inputFile = "dendrogramGroups100.json"
    outputFile = "stationsGroupedWeekdays100.json"

with open("../data/nyc/dtwClustering/weekdays/"+inputFile, "r") as f:
    groups = json.load(f)
    
with open("../data/nyc/stations.json", "r") as f:
    stations = json.load(f)
    
with open("colors.dat", "r") as f:
    colors = json.load(f)
    
stationLookup = {}

for i, station in enumerate(stations):
    stationLookup[int(station["id"])] = i
    
for i, group in enumerate(groups):
    for id in group["contents"]:
        if id in stationLookup:
            stations[stationLookup[id]]["color"] = colors[i]
        
with open("../data/nyc/dtwClustering/"+outputFile, "w") as f:
    json.dump(stations, f)