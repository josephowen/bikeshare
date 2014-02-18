import urllib
import json

response = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=20906-4738,+MD&sensor=false")
location = json.load(response)

for line in response.readlines():
	print line
	
output = open("out.txt", "w")

output.write(str(location))

print location