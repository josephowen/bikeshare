import urllib2
import json

jsonFile = urllib2.urlopen("http://citibikenyc.com/stations/json/")
data = json.load(jsonFile)
		
with open("../../data/nyc/raw/stations.json", "w") as f:
	json.dump(data["stationBeanList"], f)