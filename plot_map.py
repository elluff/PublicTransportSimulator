import json
import gmplot
from vectors import *

print "STARTING PLOT"

extended_data_filename = "61_extended_data.json"
snapper_data_filename = "snapper_data.json"

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


a = load_json(extended_data_filename)

train_array = a["data"]
users_array = a["simplified_data"]

# PLOT 
for d in train_array:
    #for vehicle in d:
        latitudes.append(float(d[0][0]))
        longitudes.append(float(d[0][1]))

gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=5)

more_lats = []
more_lngs = []


# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)


# PLOT USERS' GPS
marker_lats = []
marker_lngs = []
for users in users_array:
    for user in users:
        if user[0] >= 0:
            marker_lats.append(float(user[0]))
            marker_lngs.append(float(user[1]))

gmap.scatter(
    [marker_lats[m] for m in range(len(marker_lats)) if not m % 3],
    [marker_lngs[m] for m in range(len(marker_lngs)) if not m % 3],
    'b', size=5, marker=True)

gmap.scatter(
    [marker_lats[m] for m in range(len(marker_lats)) if not (m + 1) % 3],
    [marker_lngs[m] for m in range(len(marker_lngs)) if not (m + 1) % 3],
    'c', size=5, marker=True)

gmap.scatter(
    [marker_lats[m] for m in range(len(marker_lats)) if not (m + 2) % 3],
    [marker_lngs[m] for m in range(len(marker_lngs)) if not (m + 2) % 3],
    'm', size=5, marker=True)


# PLOT SNAPPED USERS
a = load_json(snapper_data_filename)
snapper_array = a["data"]

snapper_onboard_lats = []
snapper_onboard_lngs = []

snapper_walking_lats = []
snapper_walking_lngs = []

for snaps in snapper_array:
    for snap in snaps:
        if snap[0] >= 0:
            if snap[2] == 1:
                snapper_onboard_lats.append(float(snap[0]))
                snapper_onboard_lngs.append(float(snap[1]))
            else:
                snapper_walking_lats.append(float(snap[0]))
                snapper_walking_lngs.append(float(snap[1]))


gmap.scatter(snapper_onboard_lats, snapper_onboard_lngs, 'g', size=20, marker=False)
gmap.scatter(snapper_walking_lats, snapper_walking_lngs, 'r', size=20, marker=False)




gmap.draw("mymap.html")
print "COMPLETED"

