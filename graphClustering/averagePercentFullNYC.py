#Performance record = 246.123025201
#Laptop = 469.733035906

from datetime import datetime, date, time, timedelta
import json
from time import clock
import sys
import os

startClock = clock()

with open("../data/nyc/raw/ind_newyork.csv", "r") as f:
    for i, l in enumerate(f):
        pass
    totalLength = i+1
    
print totalLength, "lines"

input = open("../data/nyc/raw/ind_newyork.csv", "r")

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
    
# print timeLookup

dayLookup = ["weekday", "weekday", "weekday", "weekday", "weekday", "weekend", "weekend"]

timePointer = 0
numTimes = len(timeLowerLookup)

updateEvery = totalLength/100

stationLookup = {}
stationIndex = 0

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
        
    # if count % updateEvery == 0:
        # print "Adding"
        # print line
    
    line = line.split(",")
    for i in xrange(len(line)):
        line[i] = line[i].replace("\"", "")
        
    
    when = datetime.strptime(line[4], "%Y-%m-%d %H:%M:%S") + timeZoneAdjust
    whichDay = dayLookup[when.weekday()]
    
    station = line[0]
    
    if not station in stationLookup.keys():
        # print "Adding station", station
        stationLookup[station] = stationIndex
        stationIndex += 1
        
        for day in days.keys():
            # print "Adding to", day
            
            thisStation = {}
            thisStation["station"] = station
            thisStation["times"] = []
            
            current = start
            while current.date() == today:
                thisTime = {}
                timestring = time.strftime(current.time(), "%H %M %S").split()
                thisTime["hour"] = timestring[0]
                thisTime["minute"] = timestring[1]
                
                thisTime["availableBikesTotal"] = 0
                thisTime["availableDocksTotal"] = 0
                thisTime["totalDocksTotal"] = 0
                thisTime["count"] = 0
                
                thisStation["times"].append(thisTime)
                
                current += increment
                    
            days[day].append(thisStation)
        
    while not (when.time() >= timeLowerLookup[timePointer] and when.time() <= timeUpperLookup[timePointer]):
        timePointer = (timePointer+1) % numTimes
        
    # whichSlot = days[whichDay][timePointer]
        
    # if count % updateEvery == 0:
        # print "to"
        # print whichDay
        # print whichSlot["hour"] + ":" + whichSlot["minute"]
    
    # print timePointer
    # print len(days[whichDay])
    
    days[whichDay][stationLookup[station]]["times"][timePointer]["availableBikesTotal"] += int(line[1])
    days[whichDay][stationLookup[station]]["times"][timePointer]["availableDocksTotal"] += int(line[2])
    days[whichDay][stationLookup[station]]["times"][timePointer]["totalDocksTotal"] += int(line[3])
    days[whichDay][stationLookup[station]]["times"][timePointer]["count"] += 1
    
input.close()    
    
numZeros = 0
for dayKey in days.keys():
    print
    print dayKey + ":"
    day = days[dayKey]
    for station in day:
        sys.stdout.write("Station: %s       \r" % station["station"])
        sys.stdout.flush()
        for thisTime in station["times"]:
            if thisTime["totalDocksTotal"] == 0:
                # print thisTime["availableBikesTotal"], thisTime["availableBikesTotal"], thisTime["totalDocksTotal"]
                numZeros += 1
                thisTime["percentFull"] = 0.0
            else:
                thisTime["percentFull"] = float(thisTime["availableBikesTotal"])/thisTime["totalDocksTotal"]
            # print time
    
# print stationLookup

print
print numZeros, "zeros"
    
endClock = clock()
print "Parsed in", endClock-startClock, "seconds"
    
for dayKey in days.keys():
    day = days[dayKey]
    fileName = "average5min/"+dayKey+"AveragesNYC.json"
    if not os.path.exists("average5min"):
        os.mkdir("average5min")
    outputFile = open(fileName, "w")
    json.dump(day, outputFile)
    outputFile.close()
    print "Wrote", fileName
    