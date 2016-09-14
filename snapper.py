import json
from geopy.distance import vincenty

snapper_filename = "snapper_data.json"
extended_data_filename = "15_extended_data.json"

distanceError = 100

print "SNAPPING..."



def load_json(filename):
    with open(filename) as d:
        data = json.load(d)
    return data


def save_json(filename, data):
    with open(filename, "w") as f:
        f.write(json.dumps({"data": data}))


def GPSdist(usr_lat, usr_lon, stat_lat, stat_lon):
    dist = vincenty((usr_lat, usr_lon), (stat_lat, stat_lon)).meters
    return dist


def snap():
    snapped_array = []

    for step in range(len(trains_array)):
        trains = trains_array[step]
        users = users_array[step]

        snapped_step = []
        for u in range(len(users)):
            user = users[u]
            if user[0] >= 0:
                user_lat = float(user[0])
                user_lon = float(user[1])
                user_estimated_pos = None
                for train in trains:
                    train_lat = float(train[0])
                    train_lon = float(train[1])
                    dist = GPSdist(user_lat, user_lon, train_lat, train_lon)

                    if dist <= distanceError:
                        user_estimated_pos = [train_lat, train_lon, 1]

                if user_estimated_pos is None:
                    user_estimated_pos = [user_lat, user_lon, 0]

                snapped_step.append(user_estimated_pos)

        snapped_array.append(snapped_step)

    return snapped_array


a = load_json(extended_data_filename)

trains_array = a["data"]
users_array = a["simplified_data"]

snapped_data = snap()
save_json(snapper_filename, snapped_data)

print "...COMPLETED!"
