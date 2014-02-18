import matplotlib.pyplot as plot
import json

with open("data/updatedStationsNYC.json", "r") as f:
	stations = json.load(f)
	
demand = []
values = []
for station in stations:
	# print station
	demand.append(station["totalDocks"])
	values.append(station["request"])

plot.scatter(demand, values)
plot.xlabel("Station Size (Total Docks)")
plot.ylabel("Request")
plot.show()