import urllib2
import xml.etree.ElementTree as ET
import json

xmlFile = urllib2.urlopen("http://capitalbikeshare.com/data/stations/bikeStations.xml")
root = ET.fromstring(xmlFile.read())

stations = []

for station in root:
	s = {}
	for info in station:
		s[info.tag] = info.text
	stations.append(s)
		
with open("../../data/dc/raw/stations.json", "w") as f:
	json.dump(stations, f)