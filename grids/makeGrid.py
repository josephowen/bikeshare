import json
from math import ceil
import sys
import os
sys.path.insert(0, "../utilities")
from LatLongDist import getDist

gridSize = float(sys.argv[1]) #km
folder = sys.argv[2]
city = sys.argv[3]

if city == "nyc":
	north = 40.916885	
	west = -74.262139
	south = 40.493437
	east = -73.693398
elif city == "dc":
	north = 39.210975
	west = -77.454987
	south = 38.694085
	east = -76.811128

#from bottom-left to top-right
# spaceVert = (north-south)/vertInc
# spaceHoriz = (east-west)/horizInc

iterations = 40
spaceVert = (north-south)/2
vertChange = (north-south)/2
for i in range(iterations):
	dist = getDist(south, west, south+spaceVert, west)
	if dist > gridSize:
		spaceVert -= vertChange
	elif dist < gridSize:
		spaceVert += vertChange
	else:
		break
	vertChange /= 2
	
spaceHoriz = (east-west)/2
horizChange = (east-west)/2
for i in range(iterations):
	dist = getDist(south, west, south, west+spaceHoriz)
	if dist > gridSize:
		spaceHoriz -= horizChange
	elif dist < gridSize:
		spaceHoriz += horizChange
	else:
		break
	horizChange /= 2

print spaceVert, spaceHoriz

vertInc = int(ceil((north-south)/spaceVert))
horizInc = int(ceil((east-west)/spaceHoriz))

print vertInc, horizInc

# exit()

data = {}
data["type"] = "FeatureCollection"
features = data["features"] = []

for i in range(vertInc):
	for j in range(horizInc):
		feature = {}
		feature["type"] = "Feature"
		properties = feature["properties"] = {}
		properties["id"] = i*horizInc+j
		geometry = feature["geometry"] = {}
		geometry["type"] = "Polygon"
		coordinates = geometry["coordinates"] = [[]]
		
		coordinates[0].append([west + j*spaceHoriz, south + i*spaceVert])
		coordinates[0].append([west + j*spaceHoriz, south + i*spaceVert + spaceVert])
		coordinates[0].append([west + j*spaceHoriz + spaceHoriz, south + i*spaceVert + spaceVert])
		coordinates[0].append([west + j*spaceHoriz + spaceHoriz, south + i*spaceVert])
		coordinates[0].append([west + j*spaceHoriz, south + i*spaceVert])
		
		features.append(feature)


if not os.path.exists("../data/"+city+"/grids"):
	os.mkdir("../data/"+city+"/grids")
	
if not os.path.exists("../data/"+city+"/grids/"+folder):
	os.mkdir("../data/"+city+"/grids/"+folder)

with open("../data/"+city+"/grids/"+folder+"/grid_areas.json", "w") as f:
	json.dump(data, f)