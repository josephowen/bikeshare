#!/usr/bin/python

import json
from time import clock
import os
import sys
sys.path.insert(0, "../utilities")
from LatLongDist import getDist

start = clock()

def checkDistances(path, outputPath):
    with open(path+"stations.json", "r") as f:
        stations = json.load(f)

    with open(path+"suggestions.json", "r") as f:
        suggestions = json.load(f)

    numStations = len(stations)
    print numStations, "actual stations"
    print len(suggestions), "suggested stations"
    updateEvery = (numStations/100)
    stationsSoFar = 0

    allDists = {}
    
    for station in stations:
        stationsSoFar += 1
        if stationsSoFar % updateEvery == 0:
            sys.stdout.write("Creating lengths structure: %d%%        \r" % (int(float(stationsSoFar)/numStations*100)))
            sys.stdout.flush()

        alat = float(station["lat"])
        alon = float(station["lon"])
        # print actualStation["id"]

        for suggestion in suggestions:
            slat = float(suggestion["lat"])
            slon = float(suggestion["lon"])
            
            dist = getDist(alat,alon, slat,slon)

            if dist < 0.4:
                if not suggestion["id"] in allDists:
                    allDists[suggestion["id"]] = {}
                    allDists[suggestion["id"]]["votes"] = suggestion["votes"]
                    allDists[suggestion["id"]]["dists"] = {}
                allDists[suggestion["id"]]["dists"][station["id"]] = dist

    print
    
    end = clock()

    print "Took", end-start, "seconds"

    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    with open(outputPath+"lengthsStructure.json", "w") as f:
        json.dump(allDists, f)


def checkStructure(path, lengthsPath):
    with open(lengthsPath+"lengthsStructure.json", "r") as f:
        lengthsStructure = json.load(f)

    with open(path+"stations.json", "r") as f:
        stations = json.load(f)

    lookup = {}
    for i, element in enumerate(stations):
        lookup[str(element["id"])] = i
        element["request"] = 0.0

    print len(lengthsStructure), "relevant suggested stations"

    for suggestion in lengthsStructure.keys():
        suggestionData = lengthsStructure[suggestion]
        dists = suggestionData["dists"]
        if not suggestionData["votes"]:
            votes = 0.0
        else:
            votes = float(suggestionData["votes"])
        total = 0
        for actual in dists.keys():
            total += dists[actual]
        for actual in dists.keys():
            stations[lookup[actual]]["request"] += ((total-dists[actual])/total)*votes

    with open(path+"stations.json", "w") as f:
        json.dump(stations, f)

import sys
if __name__ == "__main__":
    if len(sys.argv) == 3:
        city = sys.argv[1]
    else:
        print "Using default parameters"
        city = "dc"
        
    checkDistances("../data/"+city+"/", "../data/"+city+"/requestCalculations/")
    checkStructure("../data/"+city+"/", "../data/"+city+"/requestCalculations/")
