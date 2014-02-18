#!/usr/bin/python

import urllib
import urllib2
import os
import sys
import zlib
import xml.etree.ElementTree as ET
import json
import copy
from datetime import datetime
import re

dt = datetime.now()
stationsFileName = "../data_dc/suggestions_" + dt.strftime("%Y-%m-%d_%H-%M") + ".json"
print "Going to save information to:", stationsFileName

values = {
    "S": "38.358888",
    "W": "-78.685799",
    "N": "39.800096",
    "E": "-75.367928"
}

# values = {
# 	"S" : "38.84431490005101",
# 	"W" : "-77.17251310156252",
# 	"N" : "38.93450447236391",
# 	"E" : "-76.89785489843752" }
	
myData = urllib.urlencode(values)

print myData

myHeaders = {}
myHeaders["Host"] = "mobilitylab.org"
myHeaders["Accept"] = "application/xml, text/xml"
myHeaders["Accept-Language"] = "en-US, en"
myHeaders["Accept-Encoding"] = "gzip, deflate"
myHeaders["Content-Type"] = "application/x-www-form-urlencoded"
myHeaders["X-Requested-With"] = "XMLHttpRequest"
myHeaders["Referer"] = "http://mobilitylab.org/bikearlington/cabistations/"
myHeaders["Connection"] = "keep-alive"

commentHeaders = {}
commentHeaders["Host"] = "mobilitylab.org"
commentHeaders["Accept"] = "application/xml, text/xml"
commentHeaders["Accept-Language"] = "en-US, en"
commentHeaders["Accept-Encoding"] = "gzip, deflate"
commentHeaders["Content-Type"] = "application/x-www-form-urlencoded"
commentHeaders["X-Requested-With"] = "XMLHttpRequest"
commentHeaders["Referer"] = "http://mobilitylab.org/bikearlington/cabistations/"
commentHeaders["Connection"] = "keep-alive"


def addComments(locNum, sugType, inFile, outFile):
    values = {
	"locNum" : locNum,
	"markerType" : sugType }
    
    commentData = urllib.urlencode(values)

    myRequest = urllib2.Request("http://mobilitylab.org/bikearlington/cabistations/getComments.php", data = commentData, headers = commentHeaders)

    try:
        result = urllib2.urlopen(myRequest)

        xmlFile = zlib.decompress(result.read(), 16+zlib.MAX_WBITS)
        result.close()

        jsonFile = open(inFile, "r")
        jsonData = json.load(jsonFile)
        jsonFile.close()

        allComments = []

        xmlFile = re.sub("&[aA][cC][iI][rR][cC];", "[acirc]", xmlFile)
        xmlFile = re.sub("&[nN][bB][sS][pP];", "[nbsp]", xmlFile)
        
        commentRoot = ET.fromstring(xmlFile)
        parent = commentRoot.find("usercomment")

        for child in parent:
            attr = child.attrib
            attr["text"] = child.text
            allComments.append(attr)
            
        for element in jsonData:
            if element["LocNumber"] == locNum:
                #print "Found it:", element
                element["comments"] = allComments

        jsonFile = open(outFile, "w")
        json.dump(jsonData, jsonFile)
        jsonFile.close()
        return True
    except:
        return False

myRequest = urllib2.Request("http://mobilitylab.org/bikearlington/cabistations/readMapDatabase.php",
	data = myData,
	headers = myHeaders)
	
result = urllib2.urlopen(myRequest)

if result.getcode() == 200:
    print "Successful result code"
else:
    print "Unsuccessful result code", result.getcode()

xmlFile = zlib.decompress(result.read(), 16+zlib.MAX_WBITS)
result.close()

allStations = []

root = ET.fromstring(xmlFile)

i = 0

failedNums = []
lastNum = ""

errors = ""

numChildren = len(list(root))

print numChildren, "markers"

#exit(0)

updateEvery = numChildren/100

for child in root:
    if i%updateEvery == 0:
        sys.stdout.write("Stations processing: %d%%       \r" % (int((float(i)/numChildren)*100)))
        sys.stdout.flush()
        
    attributes = child.attrib

    commentValues = {}
    commentValues["locNum"] = attributes["LocNumber"]
    lastNum = attributes["LocNumber"]
    commentValues["markerType"] = attributes["type"]
    
    commentData = urllib.urlencode(commentValues)
    
    commentRequest = urllib2.Request("http://mobilitylab.org/bikearlington/cabistations/getComments.php", data = commentData, headers = commentHeaders)
        
    allComments = []

    try:
        commentResult = urllib2.urlopen(commentRequest)
        
        commentXmlFile = zlib.decompress(commentResult.read(), 16+zlib.MAX_WBITS)
        commentResult.close()

        commentXmlFile = re.sub("&[aA][cC][iI][rR][cC];", "[acirc]", commentXmlFile)
        commentXmlFile = re.sub("&[nN][bB][sS][pP];", "[nbsp]", commentXmlFile)
    
        commentRoot = ET.fromstring(commentXmlFile)
        parent = commentRoot.find("usercomment")
    
        for child in parent:
            attr = child.attrib
            attr["text"] = child.text
            allComments.append(attr)
    except:
        errors += "Error on station:" + str(attributes["LocNumber"]) + "\n"
        failedNums.append([attributes["LocNumber"], attributes["type"]])

    attributes["comments"] = allComments

    allStations.append(attributes)
    i += 1
        
print
print errors
print "Last locNum was", lastNum

jsonFile = open(stationsFileName, "w")
json.dump(allStations, jsonFile)
jsonFile.close()

while len(failedNums) > 0:
    newFailedNums = []
    for failedNum in failedNums:
        print "Retrying station", failedNum[0]
        success = addComments(failedNum[0], failedNum[1], stationsFileName, stationsFileName)
        if success:
            print "Success"
        else:
            print "Failed on station", failedNum[0], "again"
            newFailedNums.append(copy.deepcopy(failedNum))
    failedNums = copy.deepcopy(newFailedNums)

print "Done"
