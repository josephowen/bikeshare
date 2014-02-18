import json

file1 = open("neal_data.txt", 'r')
file2 = open("joseph_data.txt", 'r')

data1 = json.load(file1)
data2 = json.load(file2)

print len(data1)
print len(data2)

file3 = open("neal_data_2.txt", 'w')
file4 = open("joseph_data_2.txt", 'w')


for item in data2:
	item.pop("phase", None)
	
json.dump(data1, file3)
json.dump(data2, file4)

