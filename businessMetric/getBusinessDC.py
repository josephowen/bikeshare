from datetime import datetime, date, time, timedelta
import json
import sys

logFileName = "../data/dc/raw/bike_ind_washingtondc.csv"


with open(logFileName, "r") as f:
    for i, l in enumerate(f):
        pass
    totalLength = i+1
    
print totalLength, "lines"

input = open(logFileName, "r")

timeZoneAdjust = timedelta(hours=-5)
# print datetime.now() + timeZoneAdjust

# start = time(0,0,0) #midnight
today = date.today()
start = datetime.combine(today, time(0,0)) #midnight
increment = timedelta(0, 300) #5 minute increments
incrementMinusOne = timedelta(0,299) #9:59

# print start
# print increment    

days = {}
days["weekday"] = []
days["weekend"] = []

timeLowerLookup = []
timeUpperLookup = []

current = start
while current.date() == today:
    timeLowerLookup.append(current.time())
    timeUpperLookup.append((current+incrementMinusOne).time())
    current += increment
    

#dayLookup = ["weekday", "weekday", "weekday", "weekday", "weekday", "weekend", "weekend"]

timePointer = 0
numTimes = len(timeLowerLookup)

updateEvery = totalLength/100

stationLast = {}
numChanges = {}
totalChange = {}
percentChange = {}
sampleCount = {}

count = 0
while 1:
    count += 1
    if count % updateEvery == 0:
        sys.stdout.write("Calculating: %d%%       \r" % (int((float(count)/totalLength)*100)))
        sys.stdout.flush()
    line = input.readline().strip()
    if line == "":
        print "Last line"
        break
    
    line = line.split("\t")
    for i in xrange(len(line)):
        line[i] = line[i].strip().replace("\"", "")
        
    
#    when = datetime.strptime(line[4], "%Y-%m-%d %H:%M:%S") + timeZoneAdjust
#    whichDay = dayLookup[when.weekday()]
    
    station = line[0]
    availableBikes = int(line[1])
    totalDocks = int(line[1])+int(line[2])
    
    if not station in stationLast:
        stationLast[station] = availableBikes
        numChanges[station] = 0
        totalChange[station] = 0
        percentChange[station] = 0
        sampleCount[station] = 1
    else:
        change = abs(availableBikes - stationLast[station])
        stationLast[station] = availableBikes
        totalChange[station] += change
        if change > 0:
            numChanges[station] += 1
        if totalDocks > 0:
            percentChange[station] += change/float(totalDocks)
        sampleCount[station] += 1
        
#    if count > 10000:
#        break
        
    
input.close()


output = {}
for station in sampleCount.keys():
    count = float(sampleCount[station])
#    print station, count
    output[station] = {"changeCount":numChanges[station]/count, "changeTotal":totalChange[station]/count, "changePercent":100*percentChange[station]/count}

with open("outputDC.json", 'w') as f:
    json.dump(output, f)