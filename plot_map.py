import json
import gmplot
from vectors import *


print "STARTING PLOT"


# extended_data_filename = "94_extended_data.json"
simulated_trains_filename = ["15_simulated_trains_gps.json",
                             "61_simulated_trains_gps.json",
                             "94_simulated_trains_gps.json"]

line_colors = ["#ff3333", "#00ff00", "#0066ff", "#ffff00"]

users_filename = "simulated_users_gps.json"


snapper_data_filename = "snapper_data.json"

gmap = gmplot.GoogleMapPlotter(45.4638768, 9.1905701, 14)


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

def get_max_snapped(snapped_user_array):
    weight = -10
    max_snap = None
    for snapped_user in snapped_user_array:
        if snapped_user[3] > weight:
            weight = snapped_user[3]
            max_snap = snapped_user
    return max_snap


lines_array = []
for line_filename in simulated_trains_filename:
    a = load_json(line_filename)
    lines_array.append([a["trains"], a["line"]])

b = load_json(users_filename)
users_array = b["users"]

# PLOT LINES
color = 0
for train_array in lines_array:
    latitudes = []
    longitudes = []
    for d in train_array[0]:
        latitudes.append(float(d[0][0]))
        longitudes.append(float(d[0][1]))

    gmap.plot(latitudes, longitudes, line_colors[color], edge_width=5)
    color += 1


# PLOT USERS' GPS
marker_lats = []
marker_lngs = []
for users in users_array:
    for user in users:
        if user[0] >= 0:
            marker_lats.append(float(user[0]))
            marker_lngs.append(float(user[1]))

num_trains = 2

gmap.scatter(
    [marker_lats[m] for m in range(len(marker_lats)) if not m % num_trains],
    [marker_lngs[m] for m in range(len(marker_lngs)) if not m % num_trains],
    'b', size=5, marker=True)

gmap.scatter(
    [marker_lats[m] for m in range(len(marker_lats)) if not (m + 1) % num_trains],
    [marker_lngs[m] for m in range(len(marker_lngs)) if not (m + 1) % num_trains],
    'c', size=5, marker=True)

# gmap.scatter(
#     [marker_lats[m] for m in range(len(marker_lats)) if not (m + 2) % num_trains],
#     [marker_lngs[m] for m in range(len(marker_lngs)) if not (m + 2) % num_trains],
#     'm', size=5, marker=True)


# PLOT SNAPPED USERS
a = load_json(snapper_data_filename)
snapper_array = a["data"]

snapper_onboard_lats = []
snapper_onboard_lngs = []

snapper_walking_lats = []
snapper_walking_lngs = []

for snaps in snapper_array:
    for s in snaps:
        snap = get_max_snapped(s)
        if snap is not None and snap[0] >= 0:
            if snap[2] is not -1:
                snapper_onboard_lats.append(float(snap[0]))
                snapper_onboard_lngs.append(float(snap[1]))
            else:
                snapper_walking_lats.append(float(snap[0]))
                snapper_walking_lngs.append(float(snap[1]))


gmap.scatter(snapper_onboard_lats,
             snapper_onboard_lngs,
             'g', size=10, marker=False)
gmap.scatter(snapper_walking_lats,
             snapper_walking_lngs,
             'r', size=10, marker=False)


gmap.draw("mymap.html")
print "COMPLETED"

