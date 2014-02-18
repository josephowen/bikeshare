import json

file = open("joseph_allData_noSpam.txt", 'r')

data = json.load(file)

total = 0
blank = 0
asdf = 0

for element in data:
	reason = element["reason"].strip()
	if len(reason) == 0:
		blank += 1
	elif "asdf" in reason:
		asdf += 1
	total += 1

print
print total, "total entries"
print asdf, "mashed entries"
print blank, "blank entries"