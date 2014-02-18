import matplotlib.pyplot as plot
import json

with open("data/updatedStationsNYC.json", "r") as f:
	stations = json.load(f)
	
demand = []
values = []
for station in stations:
	# print station
	demand.append(station["bikesChanges"])
	values.append(station["request"])

plot.scatter(demand, values)
plot.xlabel("Demand")
plot.ylabel("Request")
plot.show()