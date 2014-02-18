import json

newStations = []

with open("../data/dc/raw/suggestions.json", "r") as f:
	oldStations = json.load(f)
	
for station in oldStations:
	if station["type"] != "user-sug":
		continue

	newStation = {}
	id = str(station["LocNumber"])
	lat = float(station["lat"])
	lon = float(station["lng"])
	
	name = str(station["name"])
	
	votes = 0
	comments = []
	for comment in station["comments"]:
		newComment = {}
	
		if comment["vote"] == "dislikes":
			votes -= 1
			newComment["vote"] = -1
		else:
			votes += 1
			newComment["vote"] = 1

		newComment["user"] = comment["user"]
		newComment["text"] = comment["text"]
		comments.append(newComment)
		
	newStation["id"] = id
	newStation["lat"] = lat
	newStation["lon"] = lon
	
	newStation["name"] = name
	newStation["votes"] = votes
	
	newStation["comments"] = comments
	
	newStations.append(newStation)
	
with open("../data/dc/suggestions.json", "w") as f:
	json.dump(newStations, f)