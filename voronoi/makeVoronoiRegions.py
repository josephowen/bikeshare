from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt
import json


array = []

with open("../data/nyc/stations.json", "r") as f:
	stations = json.load(f)
	
#with open("../data/dc/stations.json", "r") as f:
#	stations = json.load(f)

for station in stations:
	array.append([station["lon"], station["lat"]])

points = np.array(array)
vor = Voronoi(points)

print vor.vertices

voronoi_plot_2d(vor)
plt.show()