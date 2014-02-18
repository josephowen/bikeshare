import matplotlib.pyplot as plot
import json

with open("data/zipcodeContents.json", "r") as f:
	zipcodes = json.load(f)
	
with open("data/demand.json", "r") as f:
	demand = json.load(f)
	
with open("data/stationsNYC.json", "r") as f:
	stations = json.load(f)
	
stationLookup = {}
for i, station in enumerate(stations):
	stationLookup[str(station["id"])] = i
	
with open("data/suggestedStationsNYC.json", "r") as f:
	suggestions = json.load(f)
	
suggestionLookup = {}
for i, suggestion in enumerate(suggestions):
	suggestionLookup[str(suggestion["id"])] = i

demandValues = []
requestValues = []
labels = []
	
for zipcode in zipcodes:
	if len(zipcodes[zipcode]["stations"]) > 0:
		demandValue = 0
		requestValue = 0
		for stationId in zipcodes[zipcode]["stations"]:
			if stationId in demand:
				demandValue += demand[stationId]
			else:
				print "Missing station", stationId
		
		for suggestionId in zipcodes[zipcode]["suggestions"]:
			thisRequest = suggestions[suggestionLookup[suggestionId]]["votes"]
			if thisRequest != None:
				requestValue += int(suggestions[suggestionLookup[suggestionId]]["votes"])
			
		demandValues.append(demandValue)
		requestValues.append(requestValue)
		labels.append(zipcode)

plot.scatter(demandValues, requestValues)
for label, x, y in zip(labels, demandValues, requestValues):
	plot.annotate(label, xy = (x,y),
		xytext = (-1, 0),
		textcoords = 'offset points', ha = 'right', va = 'bottom',
		)
plot.xlabel("Demand")
plot.ylabel("Request")
plot.show()