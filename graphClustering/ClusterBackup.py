#!/usr/bin/python
import json
import os
import sys
from time import sleep
import matplotlib.pyplot as plt
from random import random

def distance(times1, times2):
    totalDist = 0
    for i in range(len(times1)):
        totalDist += abs(times1[i]-times2[i])
    # print totalDist
    return totalDist
        
def showFigure(group1, group2):
    plt.clf()
    y = group1["times"]
    x = range(len(y))
    plt.plot(x,y, color=(random(), random(), random()))
    
    y = group2["times"]
    x = range(len(y))
    plt.plot(x,y, color=(random(), random(), random()))
    
    sleep(1.0)
    plt.draw()
    
def plotDistances(distances):
    steps = range(len(distances))
    plt.plot(steps, distances)
    plt.xlabel("Step")
    plt.ylabel("# of Distances")
#    plt.show()
    
def plotMinDistances(minDistances):
    steps = range(len(minDistances))
    plt.plot(steps, minDistances)
    plt.xlabel("Step")
    plt.ylabel("Min Distances")
#    plt.show()

def cluster(groups, maxDist):
    show = [False, 15]
    if show[0]:
        plt.ion()
        plt.xlabel("Time")
        plt.ylabel("% Full")
        plt.show()
    groupsLength = len(groups)
    updateEvery = groupsLength/100
    allDists = {}
    ids = groups.keys()
    for i, id1 in enumerate(ids):
        if i%updateEvery == 0:
            sys.stdout.write("Calculating distances: {:.2%}    \r".format(float(i)/groupsLength))
            sys.stdout.flush()
        group1 = groups[id1]
        for id2 in ids[(i+1):]:
            group2 = groups[id2]
            dist = distance(group1["times"], group2["times"])
            
            if dist > maxDist:
                continue
            if dist in allDists:
                allDists[dist].append([id1, id2])
            else:
                allDists[dist] = [[id1, id2]]
            
    print

    distEachStep = []
    minDistEachStep = []
    
    while len(allDists) > 0:
        distEachStep.append(len(allDists.keys()))
        sys.stdout.write("Distances left: %d            \r" % len(allDists.keys()))
        sys.stdout.flush()
        
        shortestDist = min(allDists.keys())
        minDistEachStep.append(shortestDist)
        #print str(shortestDist) + ":", allDists[shortestDist]
        id1, id2 = allDists[shortestDist][0]
        group1, group2 = groups[id1], groups[id2]
        if show[0] and len(groups) < show[1]:
            showFigure(group1, group2)
        #Update group1 to include group2
        # sys.stdout.write("Before: " + str(groups[id1]["times"][0]) + ", " + str(groups[id2]["times"][0]))
        group1["contents"] += group2["contents"]
        times1 = group1["times"]
        times2 = group2["times"]
        newTimes = []
        for i in range(len(times1)):
            newTimes.append((times1[i]+times2[i])/2.0)

        group1["times"] = newTimes
        #And remove group2
        del groups[id2]
        
        # sys.stdout.write(" / After: " + str(groups[id1]["times"][0]) + "\n")

        #Remove all entries with id2 in them (and all old id1 entries)
        #print "Removing all entries containing", id2, "(and", str(id1)+")"
        elemsToRemove = {}
        toReinsert = []
        for dist, pairs in allDists.iteritems():
            for i, pair in enumerate(pairs):
                if id2 in pair:
                    if not dist in elemsToRemove:
                        elemsToRemove[dist] = []
                    elemsToRemove[dist].insert(0,i)
                elif id1 in pair:
                    toReinsert.append(pair)
                    if not dist in elemsToRemove:
                        elemsToRemove[dist] = []
                    elemsToRemove[dist].insert(0,i)
        
        for dist, indices in elemsToRemove.iteritems():
            if len(indices) == len(allDists[dist]):
                #print "Removed", allDists[dist], "("+str(dist)+")"
                del allDists[dist]
            else:
                for i in indices:
                    #print "Removed", allDists[dist][i], "("+str(dist)+")"
                    del allDists[dist][i]

        #Reinsert all entries with id1 in them
        for pair in toReinsert:
            id1, id2 = pair
            group1 = groups[id1]
            group2 = groups[id2]
            dist = distance(group1["times"], group2["times"])
            if dist > maxDist:
                continue
            if dist in allDists:
                allDists[dist].append([id1, id2])
            allDists[dist] = [[id1, id2]]
            #print "Reinserted", [id1, id2], "("+str(dist)+")"
            
    print
    
    # plotDistances(distEachStep)
    plotMinDistances(minDistEachStep)

    return groups
                    
            

def run(sourceFile, destinationFolder, fileName, maxDistance):
    if not destinationFolder[-1] == "/":
        destinationFolder += "/"

    if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)
    
    with open(sourceFile, "r") as f:
        data = json.load(f)

    groups = {}
    for i, element in enumerate(data):
        thisGroup = {}
        thisGroup["contents"] = [int(element["station"])]
        times = []
        total = 0.0
        count = 0
        for j in range(len(element["times"])):
            total += element["times"][j]["percentFull"]
            count += 1
        avg = total/count
        print "Average:", avg
        if avg != 0:
            for j in range(len(element["times"])):
                times.append(element["times"][j]["percentFull"]/avg)
        else:
            for j in range(len(element["times"])):
                times.append(0.0)
        thisGroup["times"] = times
        groups[i] = thisGroup
		
    print "Before:", len(groups), "groups"
    
    # exit(0)

    groups = cluster(groups, maxDistance)
    
    groupsList = []
    for value in groups.itervalues():
        groupsList.append(value)

    fileName = destinationFolder + fileName +str(maxDistance)+".json"

    print "Writing to", fileName

    with open(fileName, "w") as f:
        json.dump(groupsList, f)
        
    print "After:", len(groups), "groups"
    
    os.system("createColors.py "+str(len(groups)))

if __name__ == "__main__":
    if len(sys.argv) == 5:
        inputFile = sys.argv[1]
        outputFolder = sys.argv[2]
        fileName = sys.argv[3]
        dist = int(sys.argv[4])
    else:
        inputFile = "../data/nyc/weekdayAverages.json"
        outputFolder = "../data/nyc/dtwClustering/weekdays"
        fileName = "dendrogramGroups"
        dist = 100
    
#    run("../data/nyc/weekdayAverages.json", "../data/nyc/dtwClustering/weekdays", "dendrogramGroups", 100)
    run(inputFile, outputFolder, fileName, dist)

