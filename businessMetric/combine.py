import json

inputFile = "output.json"
stationsFile = "../data/nyc/stations.json"

with open(inputFile, "r") as f:
    data = json.load(f)
    
with open(stationsFile, "r") as f:
    stations = json.load(f)
    
stationLookup = {}

for i, station in enumerate(stations):
    stationLookup[station["id"]] = i
    
for station in data.keys():
    if station in stationLookup:
        for (key, value) in data[station].items():
            stations[stationLookup[station]][key] = value
        
with open(stationsFile, "w") as f:
    json.dump(stations, f)