import json

file1 = open("neal_data_2.txt", 'r')
file2 = open("joseph_data_2.txt", 'r')

data1 = json.load(file1)
data2 = json.load(file2)

file1ids = []
file2ids = []

file1map = {}
file2map = {}

for key in data1:
	file1ids.append(int(key["id"]))
	file1map[int(key["id"])] = key
	
for key in data2:
	file2ids.append(int(key["id"]))
	file2map[int(key["id"])] = key
	
in1not2 = [i for i in file1ids if not i in file2ids]
in2not1 = [i for i in file2ids if not i in file1ids]

print "Neal, not Joseph:"
print in1not2
print len(in1not2)
for id in in1not2:
	print file1map[id]["lon"], file1map[id]["lat"]

print "Joseph, not Neal:"
print in2not1
print len(in2not1)
for id in in2not1:
	print file2map[id]["lon"], file2map[id]["lat"]