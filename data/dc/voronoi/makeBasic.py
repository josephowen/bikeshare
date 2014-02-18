import json

with open("voronoiInfoDC.json", 'r') as f:
    all = json.load(f)
    
features = all["features"]
for feature in features:
    feature["properties"] = {}
    
with open("voronoi.json", 'w') as f:
    json.dump(all, f)