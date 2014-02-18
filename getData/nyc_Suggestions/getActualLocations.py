import json
import urllib

file = urllib.urlopen("http://citibikenyc.com/stations/json/")

data = json.load(file)
	
outFile = open("actualStations.txt", 'w')
	
json.dump(data["stationBeanList"], outFile)

print "done"