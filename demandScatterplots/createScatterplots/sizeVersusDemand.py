import matplotlib.pyplot as plot
import json

with open("data/updatedStationsNYC.json", "r") as f:
	stations = json.load(f)
	
demand = []
size = []
for station in stations:
	# print station
	size.append(station["totalDocks"])
	demand.append(station["bikesChanges"])

plot.scatter(size, demand)
plot.xlabel("Station Size (Total Docks)")
plot.ylabel("Demand")
plot.show()