import os

def runSet(city, distance, days, distanceType):
    os.system(" ".join(["Cluster.py",
                        "../data/"+city+"/"+days+"Averages.json",
                        "../data/"+city+"/dtwClustering/"+days+" dendrogramGroups",
                        distance,
                        distanceType,
                        "../data/"+city+"/dtwClustering/"+days+"/colors"+distance+".json"
                        ]))
    os.system(" ".join(["combine.py", "../data/"+city+"/dtwClustering/"+days+"/dendrogramGroups"+distance+".json", "../data/"+city+"/stations.json", days+distance+"group"]))
    os.system(" ".join(["graphAllGroups.py", "../data/"+city+"/dtwClustering/"+days+"/dendrogramGroups"+distance+".json", "../data/"+city+"/dtwClustering/"+days+"GraphsGrouped"+distance+".png", "../data/"+city+"/dtwClustering/"+days+"/colors"+distance+".json"]))
    
#runSet("nyc", "20", "weekday", "dtw")

runSet("nyc", "50", "weekday", "ydiff")
#runSet("nyc", "50", "weekend", "ydiff")

#runSet("dc", "50", "weekday", "ydiff")
#runSet("dc", "50", "weekend", "ydiff")

#os.system("Cluster.py ../data/nyc/weekdayAverages.json ../data/nyc/dtwClustering/weekdays dendrogramGroups 100")
#os.system("combine.py ../data/nyc/dtwClustering/weekdays/dendrogramGroups100.json ../data/nyc/stations.json ../data/nyc/dtwClustering/stationsGroupedWeekdays100.json")
#os.system("graphAllGroups.py ../data/nyc/dtwClustering/weekdays/dendrogramGroups100.json ../data/nyc/dtwClustering/graphsGroupedWeekdays100.png")
#
#os.system("Cluster.py ../data/nyc/weekendAverages.json ../data/nyc/dtwClustering/weekends dendrogramGroups 100")
#os.system("combine.py ../data/nyc/dtwClustering/weekends/dendrogramGroups100.json ../data/nyc/stations.json ../data/nyc/dtwClustering/stationsGroupedWeekends100.json")
#os.system("graphAllGroups.py ../data/nyc/dtwClustering/weekends/dendrogramGroups100.json ../data/nyc/dtwClustering/graphsGroupedWeekends100.png")
#
#
#
#os.system("Cluster.py ../data/dc/weekdayAverages.json ../data/dc/dtwClustering/weekdays dendrogramGroups 100")
#os.system("combine.py ../data/dc/dtwClustering/weekdays/dendrogramGroups100.json ../data/dc/stations.json ../data/dc/dtwClustering/stationsGroupedWeekdays100.json")
#os.system("graphAllGroups.py ../data/dc/dtwClustering/weekdays/dendrogramGroups100.json ../data/dc/dtwClustering/graphsGroupedWeekdays100.png")
#
#os.system("Cluster.py ../data/dc/weekendAverages.json ../data/dc/dtwClustering/weekends dendrogramGroups 100")
#os.system("combine.py ../data/dc/dtwClustering/weekends/dendrogramGroups100.json ../data/dc/stations.json ../data/dc/dtwClustering/stationsGroupedWeekends100.json")
#os.system("graphAllGroups.py ../data/dc/dtwClustering/weekends/dendrogramGroups100.json ../data/dc/dtwClustering/graphsGroupedWeekends100.png")