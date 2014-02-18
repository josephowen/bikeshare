import matplotlib.path as path
import json

with open("../data/dc/voronoi/voronoi.json", "r") as f:
    voronois = json.load(f)

with open("../data/dc/suggestions.json", "r") as f:
    suggestions = json.load(f)

with open("../data/dc/stations.json", "r") as f:
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
        
totalLength = len(voronois["features"])

insideVoronois = {}

for i, feature in enumerate(voronois["features"]):
    docks = 0
    votes = 0

    vorPath = feature["geometry"]["coordinates"]
    while len(vorPath[0]) != 2:
        vorPath = vorPath[0]
    vorPath = path.Path(vorPath)

    stationsInside = []
    points = vorPath.contains_points(staPointArray)
    for j in range(len(points)):
        if points[j]:
            stationsInside.append(staIdArray[j])
            docks += docksArray[j]
            
    if len(stationsInside) != 1:
        print "ERROR"

    if not stationsInside[0] in insideVoronois:
        thisZipcode = insideVoronois[stationsInside[0]] = {}
        thisZipcode["stations"] = []
        thisZipcode["suggestions"] = []
    else:
        thisZipcode = insideVoronois[stationsInside[0]]
            
    suggestionsInside = []
    points = vorPath.contains_points(sugPointArray)
    for j in range(len(points)):
        if points[j]:
            suggestionsInside.append(sugIdArray[j])
            votes += votesArray[j]
    
    thisZipcode["stations"] += stationsInside
    thisZipcode["suggestions"] += suggestionsInside
    
    feature["properties"]["totalDocks"] = docks
    feature["properties"]["votes"] = votes
    
    print str(i+1) + "/" + str(totalLength) + ": ", len(stationsInside), "stations and", len(suggestionsInside), "suggestions, " + str(docks) + " totalDocks, " + str(votes) + " votes"
    
with open("../data/dc/voronoi/voronoiContents.json", "w") as f:
    json.dump(insideVoronois, f)
    
    
with open("../data/dc/voronoi/voronoiInfo.json", "w") as f:
    json.dump(voronois, f)