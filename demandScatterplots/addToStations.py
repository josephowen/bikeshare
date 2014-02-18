import json

with open("data/updatedStationsNYC.json", "r") as f:
	stations = json.load(f)
	
with open("data/demand2.json", "r") as f:
	newData = json.load(f)


for station in stations:
	if str(station["id"]) in newData:
		station["monDemand2"] = newData[str(station["id"])]
	else:
		station["monDemand2"] = 0
		print "Added 0 for", station["id"]

with open("data/updatedStationsMonDemandNYC.json", "w") as f:
	json.dump(stations, f)