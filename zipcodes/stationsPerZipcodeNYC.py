import matplotlib.path as path
import json

with open("../data/nyc/zipcodes/zipcodes.json", "r") as f:
    zipcodes = json.load(f)

with open("../data/nyc/suggestions.json", "r") as f:
    suggestions = json.load(f)

with open("../data/nyc/stations.json", "r") as f:
    stations = json.load(f)
    
staPointArray = []
staIdArray = []
docksArray = []
for station in stations:
    staPointArray.append([station["lon"], station["lat"]])
    staIdArray.append(station["id"])
    docksArray.append(station["totalDocks"])

sugPointArray = []
sugIdArray = []
votesArray = []
for suggestion in suggestions:
    sugPointArray.append([suggestion["lon"], suggestion["lat"]])
    sugIdArray.append(suggestion["id"])
    votesArray.append(suggestion["votes"])
        
totalLength = len(zipcodes["features"])

insideZipcodes = {}

for i, feature in enumerate(zipcodes["features"]):
    docks = 0
    votes = 0

    zipPath = feature["geometry"]["coordinates"]
    while len(zipPath[0]) != 2:
        zipPath = zipPath[0]
    zipPath = path.Path(zipPath)

    stationsInside = []
    points = zipPath.contains_points(staPointArray)
    for j in range(len(points)):
        if points[j]:
            stationsInside.append(staIdArray[j])
            docks += docksArray[j]

    if not feature["properties"]["ZIP"] in insideZipcodes:
        thisZipcode = insideZipcodes[feature["properties"]["ZIP"]] = {}
        thisZipcode["stations"] = []
        thisZipcode["suggestions"] = []
    else:
        thisZipcode = insideZipcodes[feature["properties"]["ZIP"]]
            
    suggestionsInside = []
    points = zipPath.contains_points(sugPointArray)
    for j in range(len(points)):
        if points[j]:
            suggestionsInside.append(sugIdArray[j])
            votes += votesArray[j]
    
    thisZipcode["stations"] += stationsInside
    thisZipcode["suggestions"] += suggestionsInside
    
    feature["properties"]["totalDocks"] = docks
    feature["properties"]["votes"] = votes
    
    print str(i+1) + "/" + str(totalLength) + ": ", len(stationsInside), "stations and", len(suggestionsInside), "suggestions, " + str(docks) + " totalDocks, " + str(votes) + " votes"
    
with open("../data/nyc/zipcodes/zipcodesContents.json", "w") as f:
    json.dump(insideZipcodes, f)
    
    
with open("../data/nyc/zipcodes/zipcodesInfo.json", "w") as f:
    json.dump(zipcodes, f)