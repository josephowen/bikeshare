import os

os.system("combine.py dendrogramGroups100.json stationsGroupedWeekdays100.json")
os.system("graphAllGroups.py weekdays/dendrogramGroups100.json")