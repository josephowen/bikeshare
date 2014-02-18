import json

file = open("joseph_allData_noSpam.txt", 'r')

data = json.load(file)

names = []

total = 0
unique = 0
blank = 0

for element in data:
	name = element["user_name"].strip()
	
	if name in names:
		if len(name) > 0:
			print name
		else:
			blank += 1
	else:
		names.append(name)
		unique += 1
	total += 1
	
print unique, "unique names in", total, "entries"
print blank, "blank name fields"