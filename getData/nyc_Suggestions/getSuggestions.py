import json
import urllib2
import copy

locFile = urllib2.urlopen("http://a841-tfpweb.nyc.gov/bikeshare/get_suggestion_points")
data = json.load(locFile)

allData = []
failures = []

for key in data:
	id = key["id"]
	print "Reading data for suggestion", id
	try:
		suggestion = urllib2.urlopen('http://a841-tfpweb.nyc.gov/bikeshare/get_suggestion_info?point='+id)
		suggestion = json.load(suggestion)
		allData.append(suggestion)
	except:
		print "failed"
		failures.append(id)
		
while len(failures) > 0:
	newFailures = []
	for id in failures:
		print "Reading data for suggestion", id
		try:
			suggestion = urllib2.urlopen('http://a841-tfpweb.nyc.gov/bikeshare/get_suggestion_info?point='+id)
			suggestion = json.load(suggestion)
			allData.append(suggestion)
		except:
			print "failed"
			newFailures.append(id)
	failures = newFailures
	
with open("../../data/nyc/raw/suggestions.json", 'w') as f:
	json.dump(allData, f)

print "done"