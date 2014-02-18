import json
import urllib

file = open("joseph_data_2.txt", 'r')

data = json.load(file)

allData = []

for key in data:
	id = key["id"]
	print "Reading data for suggestion", id
	suggestion = urllib.urlopen('http://a841-tfpweb.nyc.gov/bikeshare/get_suggestion_info?point='+id)
	suggestion = json.load(suggestion)
	allData.append(suggestion)
	
outFile = open("joseph_allData.txt", 'w')
	
json.dump(allData, outFile)

print "done"