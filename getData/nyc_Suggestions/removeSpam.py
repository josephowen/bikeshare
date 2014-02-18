import json

file = open("joseph_allData.txt", 'r')

data = json.load(file)

newData = []

numRemoved = 0

for element in data:
	if (element["lat"] == "0" or element["lon"] == "0"):
		print "Removing id", element["id"]
		numRemoved += 1
	else:
		newData.append(element)
	
outFile = open("joseph_allData_noSpam.txt", 'w')
	
json.dump(newData, outFile)

print "Removed", numRemoved, "elements"
print "Done"