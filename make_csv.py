import json
import csv

inputFile =  "data/dc/stations.json"
outputName = "test.csv"

columns = ["id", "docks", "request", "changeCount", "changeTotal", "changePercent", "elev"]

with open(inputFile, "r") as f:
    data = json.load(f)
    

outputFile = open(outputName, "wb")
writer = csv.writer(outputFile) #, delimiter='\t')

writer.writerow(columns)

for element in data:
    row = []
    try:
        for col in columns:
            row.append(element[col])
        writer.writerow(row)
    except:
        continue
    
outputFile.close()