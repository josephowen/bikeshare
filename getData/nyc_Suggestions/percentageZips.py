import json
import re

zipRE = re.compile(r"(?:^\d{5}$)|(?:^\d{5}-\d{4}$)")
zipPlusFourRE = re.compile(r"^\d{5}-\d{4}$")
closeRE = re.compile(r"(?:^\d{4}$)|(?:^\w{3}\s?\w{3}$)")
notCloseRE = re.compile(r"[A-Z][a-z]{5}")

file = open("joseph_allData_noSpam.txt", 'r')

data = json.load(file)

total = 0
zips = 0
zipsPlusFour = 0
blank = 0
illegal = 0
close = 0

for element in data:
	zip = element["user_zip"].strip()
	if not zipRE.match(zip):
		if len(zip) > 0:
			illegal += 1
			if closeRE.match(zip) and not notCloseRE.match(zip):
				close += 1
			else:
				print zip
		else:
			blank += 1
	else:
		if zipPlusFourRE.match(zip):
			zipsPlusFour += 1
		zips += 1
	total += 1

print
print total, "total entries"
print zips, "legal zipcodes"
print " ", zipsPlusFour, "of which are zips plus four"
print illegal, "illegal entries"
print " ", close, "valiant attempts"
print blank, "blank entries"