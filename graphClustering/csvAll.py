import json
import sys
import csv

outFile = open(sys.argv[2], "wb")
writer = csv.writer(outFile)

with open(sys.argv[1], "r") as f:
    stations = json.load(f)

allStations = []
allRows = []
first = True

for station in stations:
    allStations.append(station["station"])
    for i, thisTime in enumerate(station["times"]):
        if first:
            allRows.append([])
        allRows[i].append(str(thisTime["percentFull"]))
    first = False

# print ", ".join(allStations)
# outFile.write(", ".join(allStations) + "\n")
# for row in allRows:
    # print ", ".join(row)
    # outFile.write(", ".join(row) + "\n")
    
writer.writerow(allStations)
for row in allRows:
    writer.writerow(row)

outFile.close()