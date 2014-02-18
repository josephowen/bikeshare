import json

newStations = []

with open("actualStationsNYC.json", "r") as f:
	oldStations = json.load(f)
	
for station in oldStations:
	newStation = {}
	id = str(station["id"])
	lat = float(station["latitude"])
	lon = float(station["longitude"])
	
	bikes = int(station["availableBikes"])
	docks = int(station["availableDocks"])
	totalDocks = int(station["totalDocks"])
	
	elev = float(0) #float(station["elev"])
	
	name = str(station["stationName"])
	
	newStation["id"] = id
	newStation["lat"] = lat
	newStation["lon"] = lon
	newStation["bikes"] = bikes
	newStation["docks"] = docks
	newStation["totalDocks"] = totalDocks
	newStation["elev"] = elev
	newStation["name"] = name
	
	newStations.append(newStation)
	
with open("stationsNYC.json", "w") as f:
	json.dump(newStations, f)