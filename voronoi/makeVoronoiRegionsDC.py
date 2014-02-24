from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt
import json

voronoiData = {}
voronoiData["type"] = "FeatureCollection"
voronoiData["features"] = []

array = []
	
with open("../data/dc/stations.json", "r") as f:
	stations = json.load(f)

for station in stations:
	array.append([station["lon"], station["lat"]])

points = np.array(array)
vor = Voronoi(points)

#print len(vor.vertices)

#print vor.regions[100]

for region in vor.regions:
	if len(region) > 0:
		feature = {"type":"Feature", "properties":{}, "geometry":{"type":"Polygon", "coordinates":[]}}
		coordinates = []
		for i in region:
			coordinates.append([vor.vertices[i][0], vor.vertices[i][1]])
			
		coordinates.append([vor.vertices[region[0]][0], vor.vertices[region[0]][1]])
			
		feature["geometry"]["coordinates"].append(coordinates)
		voronoiData["features"].append(feature)

with open("../data/dc/voronoi/voronoi.json", "w") as f:
	json.dump(voronoiData, f)

voronoi_plot_2d(vor)
plt.show()