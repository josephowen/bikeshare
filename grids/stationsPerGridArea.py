import matplotlib.path as path
import json
import sys

folder = sys.argv[1].strip("/")
city = sys.argv[2].strip("/")

with open("../data/"+city+"/grids/"+folder+"/grid_areas.json", "r") as f:
	gridAreas = json.load(f)

with open("../data/"+city+"/suggestions.json", "r") as f:
	suggestions = json.load(f)

with open("../data/"+city+"/stations.json", "r") as f:
	stations = json.load(f)
	
staPointArray = []
staIdArray = []
for station in stations:
	staPointArray.append([station["lon"], station["lat"]])
	staIdArray.append(str(station["id"]))

sugPointArray = []
sugIdArray = []
for suggestion in suggestions:
	sugPointArray.append([suggestion["lon"], suggestion["lat"]])
	sugIdArray.append(str(suggestion["id"]))
		
totalLength = len(gridAreas["features"])
updateEvery = totalLength / 100

insideGridAreas = {}

for i, feature in enumerate(gridAreas["features"]):
	if not feature["properties"]["id"] in insideGridAreas:
		thisGridAreas = insideGridAreas[feature["properties"]["id"]] = {}
		thisGridAreas["stations"] = []
		thisGridAreas["suggestions"] = []

	gridAreaPath = feature["geometry"]["coordinates"]
	while len(gridAreaPath[0]) != 2:
		gridAreaPath = gridAreaPath[0]
	gridAreaPath = path.Path(gridAreaPath)
	
	stationsInside = []
	points = gridAreaPath.contains_points(staPointArray)
	for j in range(len(points)):
		if points[j]:
			stationsInside.append(staIdArray[j])
			
	suggestionsInside = []
	points = gridAreaPath.contains_points(sugPointArray)
	for j in range(len(points)):
		if points[j]:
			suggestionsInside.append(sugIdArray[j])
	
	thisGridAreas["stations"] += stationsInside
	thisGridAreas["suggestions"] += suggestionsInside
	if i%updateEvery == 0:
		sys.stdout.write("Grid Areas processing: %d%%       \r" % (int((float(i)/totalLength)*100)))
		sys.stdout.flush()
	# print str(i+1) + "/" + str(totalLength) + ": ", len(stationsInside), "stations and", len(suggestionsInside), "suggestions"
	
print
	
with open("../data/"+city+"/grids/"+folder+"/gridAreaContents.json", "w") as f:
	json.dump(insideGridAreas, f)