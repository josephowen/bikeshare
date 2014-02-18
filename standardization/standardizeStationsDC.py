import json
import urllib2

newStations = []

with open("../data/dc/raw/stations.json", "r") as f:
	oldStations = json.load(f)
	
for station in oldStations:
	newStation = {}
	id = str(station["id"])
	lat = float(station["lat"])
	lon = float(station["long"])
	
	bikes = int(station["nbBikes"])
	docks = int(station["nbEmptyDocks"])
	totalDocks = bikes+docks
	
#	elev = float(station["elev"])
	
	name = str(station["name"])
	
	newStation["id"] = id
	newStation["lat"] = lat
	newStation["lon"] = lon
	newStation["bikes"] = bikes
	newStation["docks"] = docks
	newStation["totalDocks"] = totalDocks
	newStation["elev"] = None
	newStation["name"] = name
	
	newStations.append(newStation)
	
	
while True:
	failCount = 0
	for i, station in enumerate(newStations):
		if station["elev"] == None:
			try:
				print "Finding elevation for station", station["id"]
				url = 'http://maps.googleapis.com/maps/api/elevation/json?locations='+str(station["lat"])+','+str(station["lon"])+'&sensor=false'
				elevPage = urllib2.urlopen(url)
				elevData = json.load(elevPage)
				elevation = elevData["results"][0]["elevation"]
				newStations[i]["elev"] = elevation
			except:
				failCount += 1
	if failCount == 0:
		break
	else:
		print failCount, "failures to find elevation, trying them again"
		
	
with open("../data/dc/stations.json", "w") as f:
	json.dump(newStations, f)