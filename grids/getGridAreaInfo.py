import matplotlib.path as path
import json
import sys

folder = sys.argv[1]
city = sys.argv[2]

with open("../data/"+city+"/grids/"+folder+"/grid_areas.json", "r") as f:
	gridAreas = json.load(f)
	
with open("../data/"+city+"/grids/"+folder+"/gridAreaContents.json", "r") as f:
	contents = json.load(f)

with open("../data/"+city+"/suggestions.json", "r") as f:
	suggestions = json.load(f)

with open("../data/"+city+"/stations.json", "r") as f:
	stations = json.load(f)
	
stationLookup = {}
for station in stations:
	stationLookup[str(station["id"])] = station["totalDocks"]
	
suggestionLookup = {}
for suggestion in suggestions:
	if suggestion["votes"] == None:
		suggestionLookup[str(suggestion["id"])] = 0
	else:
		suggestionLookup[str(suggestion["id"])] = int(suggestion["votes"])
	
for feature in gridAreas["features"]:
	id = str(feature["properties"]["id"])
	stationList = contents[id]["stations"]
	suggestionList = contents[id]["suggestions"]
	
	bikedocks = 0
	votes = 0
	
	for station in stationList:
		if station in stationLookup:
			bikedocks += stationLookup[station]
			
	for suggestion in suggestionList:
		if suggestion in suggestionLookup:
			votes += suggestionLookup[suggestion]
	
	feature["properties"]["BIKEDOCKS"] = bikedocks
	feature["properties"]["VOTES"] = votes

with open("../data/"+city+"/grids/"+folder+"/grid_areas_info.json", "w") as f:
	json.dump(gridAreas, f)