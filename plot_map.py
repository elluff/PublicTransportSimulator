import json
import gmplot
from vectors import *

print "STARTING PLOT"

gmap = gmplot.GoogleMapPlotter(45.4638768, 9.1905701, 14)

latitudes = []
longitudes = []


def load_json(filename):
    with open(filename) as d:
        data = json.load(d)
    return data


def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0 / line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)


a = load_json("extended_data.json")

data = a["data"]
users = a["simplified_data"]

for d in data:
    #for vehicle in d:
        latitudes.append(float(d[0][0]))
        longitudes.append(float(d[0][1]))

gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=5)

more_lats = []
more_lngs = []


#gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)

marker_lats = []
marker_lngs = []
for user in users: 
        marker_lats.append(float(user[0][0]))
        marker_lngs.append(float(user[0][1]))
gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)


# heat_lats = [43.5]
# heat_lngs = [7.5]
# gmap.heatmap(heat_lats, heat_lngs)
gmap.draw("mymap.html")
print "COMPLETED"

