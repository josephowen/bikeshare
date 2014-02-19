#!/usr/bin/python
import json
import os
import sys
from LatLongDist import getDist

def cluster(groups, maxDist):
    groupsLength = len(groups)
    updateEvery = groupsLength/100
    allDists = {}
    ids = groups.keys()
    for i, id1 in enumerate(ids):
        if i%updateEvery == 0:
            sys.stdout.write("Distance calculation: %d%%    \r" % (int((float(i)/groupsLength)*100)))
            sys.stdout.flush()
        group1 = groups[id1]
        for id2 in ids[(i+1):]:
            group2 = groups[id2]
            dist = getDist(group1["lat"],group1["lon"], group2["lat"],group2["lon"])
            #if (id1==845 and id2==279) or (id1==279 and id2==845):
            #    print "HERE IT IS:", dist
            if dist > maxDist:
                continue
            if dist in allDists:
                allDists[dist].append([id1, id2])
            else:
                allDists[dist] = [[id1, id2]]

    print

    while len(allDists) > 0:
        sys.stdout.write("Distances left: %d            \r" % len(allDists.keys()))
        sys.stdout.flush()

        shortestDist = min(allDists.keys())
        #print str(shortestDist) + ":", allDists[shortestDist]
        id1, id2 = allDists[shortestDist][0]
        group1, group2 = groups[id1], groups[id2]
        #print group1, group2
        
        #Update group1 to include group2
        group1["contents"] += group2["contents"]
        group1Votes = group1["votes"]
        totalVotes = group1Votes + group2["votes"]
        ratio = float(group1Votes)/totalVotes
        lat2, lon2 = group2["lat"], group2["lon"]
        midLat = lat2 + ratio*(group1["lat"]-lat2)
        midLon = lon2 + ratio*(group1["lon"]-lon2)
        group1["votes"] = totalVotes
        group1["lat"] = midLat
        group1["lon"] = midLon

        #And remove group2
        del groups[id2]

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
            dist = getDist(group1["lat"],group1["lon"], group2["lat"],group2["lon"])
            if dist > maxDist:
                continue
            if dist in allDists:
                allDists[dist].append([id1, id2])
            allDists[dist] = [[id1, id2]]
            #print "Reinserted", [id1, id2], "("+str(dist)+")"
            
    print

    return groups
                    
            

def run(sourceFile, destinationFolder, maxDistance):
    if not destinationFolder[-1] == "/":
        destinationFolder += "/"

    if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)
    
    with open(sourceFile, "r") as f:
        data = json.load(f)

    groups = {}
    for i, element in enumerate(data):
        thisGroup = {}
        thisGroup["contents"] = [int(element["id"])]
        thisGroup["lat"] = float(element["lat"])
        thisGroup["lon"] = float(element["lon"])
        thisGroup["votes"] = max(element["votes"]+1, 1)
        groups[i] = thisGroup
		
    print "Before:", len(groups), "groups"

    groups = cluster(groups, maxDistance)
    
    groupsList = []
    for value in groups.itervalues():
        groupsList.append(value)

    #print len(groups), "groups remaining"

    fileName = destinationFolder + "dendrogramGroups"+str(int(maxDistance*1000))+"meters.json"

    print "Writing to", fileName

    with open(fileName, "w") as f:
        json.dump(groupsList, f)
        
    print "After:", len(groups), "groups"

if __name__ == "__main__":
    run("../data/nyc/suggestions.json", "../data/nyc/clustering", 0.050)
#    run("../data/nyc/suggestions.json", "../data/nyc/clustering", 0.100)
    run("../data/nyc/suggestions.json", "../data/nyc/clustering", 0.150)
    run("../data/nyc/suggestions.json", "../data/nyc/clustering", 0.200)
	
    run("../data/dc/suggestions.json", "../data/dc/clustering", 0.050)
#    run("../data/dc/suggestions.json", "../data/dc/clustering", 0.100)
    run("../data/dc/suggestions.json", "../data/dc/clustering", 0.150)
    run("../data/dc/suggestions.json", "../data/dc/clustering", 0.200)

