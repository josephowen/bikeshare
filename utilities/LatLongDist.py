#!/usr/bin/python
import numpy as np

def getDist(lat1, lon1, lat2, lon2):
	# cdef float lat1, lon1 = start
	# cdef float lat2, lon2 = end
	
	#Code for distance from latitude, longitude pair.
	#Adapted from http://www.movable-type.co.uk/scripts/latlong.html
	R = 6371 #km
	dLat = np.radians(lat2-lat1)
	dLon = np.radians(lon2-lon1)
	lat1 = np.radians(lat1)
	lat2 = np.radians(lat2)
	a = np.sin(dLat/2) * np.sin(dLat/2) + np.sin(dLon/2) * np.sin(dLon/2) * np.cos(lat1) * np.cos(lat2)
	c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
	return R * c
