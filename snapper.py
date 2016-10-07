import json
from geopy.distance import vincenty

snapper_filename = "snapper_data.json"
users_filename = "simulated_users_gps.json"

simulated_trains_filename = ["15_simulated_trains_gps.json",
                             "61_simulated_trains_gps.json",
                             "94_simulated_trains_gps.json"]

max_weight = 20
distanceError = 100

incr_weight = 2
decr_weight = 1

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


def get_snapped_info(snapped_user_array, line):
    for snapped_user in snapped_user_array:
        if snapped_user[2] == line:
            return snapped_user
    return None


def get_max_snapped(snapped_user_array):
    weight = -10
    max_snap = None
    for snapped_user in snapped_user_array:
        if snapped_user[3] > weight:
            weight = snapped_user[3]
            max_snap = snapped_user
    return max_snap


def get_closest_train_pos(snapped_user_array):
    weight = -10
    max_snap = None
    for snapped_user in snapped_user_array:
        if snapped_user[3] > weight:
            weight = snapped_user[3]
            max_snap = snapped_user
    return max_snap


def snap():
    snapped_array = []

    for step in range(len(lines_array[0][0])):
        # trains_step = []
        # mange linename
        # print lines_array

        users = users_array[step]
        snapped_step = []

        for u in range(len(users)):
            user = users[u]

            if user[0] < 0:
                weight = 0
                if len(snapped_array) > 0:
                    weight = max(0, get_max_snapped(snapped_array[step - 1][u])[3] - decr_weight)
                if weight > 0:
                    snapped_step.append([[snapped_array[step - 1][u][0],
                                         snapped_array[step - 1][u][1],
                                         snapped_array[step - 1][u][2],
                                         weight, None]])
                else:
                    snapped_step.append([[-1, -1, -1, 0, None]])
            else:
                user_estimated_pos = []
                # min_dist = distanceError + 1

                user_lat = float(user[0])
                user_lon = float(user[1])

                for trains_array in lines_array:
                    trains_step = trains_array[0][step]

                    # for trains in [t for sub in trains_step for t in sub]:
                    # print trains

                    for tr_pos in range(len(trains_step)):
                        train = trains_step[tr_pos]
                        train_lat = float(train[0])
                        train_lon = float(train[1])
                        dist = GPSdist(user_lat, user_lon,
                                       train_lat, train_lon)

                        if dist <= distanceError:  # and dist < min_dist:
                            # if len(snapped_array) > 0 and snapped_array[step - 1][u][2] == trains_array[1]:

                            sn_arr = None
                            if len(snapped_array):
                                sn_arr = get_snapped_info(snapped_array[step - 1][u], trains_array[1])
                            if sn_arr is None:
                                sn_arr = [0, 0, 0, 0, None]
                            weight = min(max_weight, sn_arr[3] + incr_weight)
                            # snapped_array[step - 1][u][3] + incr_weight)
                            user_estimated_pos.append([train_lat,
                                                       train_lon,
                                                       trains_array[1],
                                                       weight,
                                                       tr_pos])
                            #    break
                            # elif dist < min_dist:
                            #     user_estimated_pos = [train_lat,
                            #                          train_lon,
                            #                          trains_array[1], incr_weight]
                            # min_dist = dist

                if len(user_estimated_pos) == 0:
                    weight = 0

                    user_estimated_pos = [[user_lat, user_lon, -1, 0, None]]
                    if len(snapped_array) > 0:
                        max_snapped = get_max_snapped(snapped_array[step - 1][u])

                        if max_snapped is not None and max_snapped[3] > 0:
                            for tr_arr in lines_array:
                                if tr_arr[1] == max_snapped[2]:
                                    # use tr_arr to get updated lat and lon

                                    user_estimated_pos = [[max_snapped[0],
                                                          tr_arr[0][step - 1][max_snapped[4]][0],
                                                          tr_arr[0][step - 1][max_snapped[4]][1],
                                                          #max_snapped[1],
                                                          #max_snapped[2],
                                                          max_snapped[3] - decr_weight,
                                                          max_snapped[4]]]
                                    break

                snapped_step.append(user_estimated_pos)
                # print user_estimated_pos[3]

        snapped_array.append(snapped_step)

    return snapped_array


lines_array = []
for line_filename in simulated_trains_filename:
    a = load_json(line_filename)
    lines_array.append([a["trains"], a["line"]])

b = load_json(users_filename)
users_array = b["users"]

snapped_data = snap()
save_json(snapper_filename, snapped_data)

print "...COMPLETED!"
