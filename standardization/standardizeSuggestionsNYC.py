import json

newStations = []

with open("../data/nyc/raw/suggestions.json", "r") as f:
	oldStations = json.load(f)
	
for station in oldStations:
	newStation = {}
	id = str(station["id"])
	lat = float(station["lat"])
	lon = float(station["lon"])
	
	# bikes = int(station["availableBikes"])
	# docks = int(station["availableDocks"])
	# totalDocks = int(station["totalDocks"])
	
	# elev = float(0) #float(station["elev"])
	
	name = str(station["neighborhood"])
	
	if station["ck_rating_up"] == None:
		votes = 0
	else:
		votes = int(station["ck_rating_up"])
	
	user_name = station["user_name"]
	user_zip = station["user_zip"]
	# user_avatar = station["user_avatar_url"]
	# user_profile = station["user_profile_url"]
	
	reason = station["reason"]
	
	# user["name"] = user_name
	# user["zip"] = user_zip
	# user["avatar"] = user_avatar
	# user["profile"] = user_profile
		
	newStation["id"] = id
	newStation["lat"] = lat
	newStation["lon"] = lon
	
	newStation["name"] = name
	newStation["votes"] = votes
	
	newStation["user_name"] = user_name
	newStation["user_zip"] = user_zip
	# newStation["bikes"] = bikes
	# newStation["docks"] = docks
	# newStation["totalDocks"] = totalDocks
	# newStation["elev"] = elev

	newStation["reason"] = reason
	
	newStations.append(newStation)
	
with open("../data/nyc/suggestions.json", "w") as f:
	json.dump(newStations, f)