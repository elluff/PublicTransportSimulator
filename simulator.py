import simpy
import json
from random import randint

import shared_data as sd

from train import Train
from user import User


station_rand = True
station_base = 30
station_delta = 90

station_incr = 0

FULL_DATA = True

simulator_filename = "_simulated_data.json"
# simulator_extended_filename = "_extended_data.json"

simulator_trains_filename = "_simulated_trains_gps.json"
simulator_users_filename = "simulated_users_gps.json"


def save_data_to_file(env, delta_t=30, full_data=FULL_DATA):
    yield env.timeout(delta_t)
    waiting_time_array = []
    waiting_time_simplified = []

    for line in sd.lines:
        sd.gps_trains_position[line] = []
    sd.gps_users_position = []

    while sd.arrived_vehicles[line] < sd.num_vehicles:

        sd.gps_users_position.append([usr[:] for usr in sd.users_pos_array])

        with open(simulator_users_filename, "w") as f:
            f.write(json.dumps({"users": sd.gps_users_position}))

        if station_rand:
            sd.station_stop = randint(station_base, station_base + station_delta)
        else:
            sd.station_stop += station_incr

        for line in sd.lines:
            if full_data:
                waiting_time = print_waiting_times(env, line)
            else:
                waiting_time = print_arrival_at_station(env, line)

            waiting_time_array.append({
                "stations": waiting_time,
                "id": "sim_line_" + line})
            waiting_time_simplified.append(waiting_time)
            save_wt_file(line + simulator_filename, waiting_time_array, waiting_time_simplified)

            sd.gps_trains_position[line].append(relPosToGps(line))

            with open(line + simulator_trains_filename, "w") as f:
                f.write(json.dumps({"trains": sd.gps_trains_position[line], "line": line}))

        yield env.timeout(delta_t)


# vehicle_in_station = [0 for _ in range(sd.n_stations)]

def print_waiting_times(env, line):

    waiting_time = []
    for station in range(sd.n_stations[line]):
        vehicle = getClosestVehicle(station, line)
        if vehicle is None or vehicle > sd.segment_length * sd.n_stations[line]:
            waiting_time.append(-1)
        elif vehicle == sd.segment_length * station:
            waiting_time.append(0)
        else:
            total_dist = abs(sd.segment_length * station - vehicle)

            if (vehicle >= 0):
                wt = 0
                # segment = vehicle // segment_length
                curr_segment = station - 1
                while curr_segment > vehicle // sd.segment_length:
                    speed = sd.speed_d if curr_segment % 2 else sd.speed_p
                    wt += sd.segment_length / speed + sd.station_stop
                    total_dist -= sd.segment_length
                    curr_segment -= 1

                # if we are in a station
                if total_dist == 0:
                    wt -= sd.station_stop / 2

                speed = sd.speed_d if (vehicle // sd.segment_length) % 2 else sd.speed_p
                wt += total_dist / speed
                waiting_time.append(round(wt / 60))
            else:
                waiting_time.append(round((total_dist / sd.starting_speed) / 60))

    return waiting_time


def print_arrival_at_station(env, line):

    waiting_time = []
    for station in range(sd.n_stations[line]):
        vehicle = getClosestVehicle(station, line)
        if vehicle is None or vehicle > sd.segment_length * sd.n_stations[line]:
            waiting_time.append(-1)
        elif vehicle == sd.segment_length * station:
            # vehicle in station
            waiting_time.append(0)
        else:
            waiting_time.append(1)

    return waiting_time


def getClosestVehicle(station, line):
    trains = list(filter(lambda x: x <= station * sd.segment_length, sd.vehicles_pos_array[line]))
    if len(trains):
        return max(trains)
    else:
        return None


def load_json(filename):
    with open(filename) as d:
        data = json.load(d)
    return data


def relPosToGps(line):
    gps_pos = []
    for vehicle in sd.vehicles_pos_array[line]:
        last_passed_station = int(vehicle / sd.segment_length) # round to lower integer
        if vehicle < 0 or vehicle > sd.segment_length * sd.n_stations[line]:
            gps_pos.append([-1, -1])
        elif vehicle == sd.segment_length * last_passed_station:
            # vehicle in station
            gps_pos.append([sd.stations_gps_pos[line][last_passed_station][2], sd.stations_gps_pos[line][last_passed_station][3]])
        else:
            percentage = (vehicle - last_passed_station * sd.segment_length) / sd.segment_length
            gps_pos.append(interoplate_gps_position(line, last_passed_station, percentage))

    return gps_pos

def interoplate_gps_position(line, last_passed_station, percentage):
    station1 = sd.stations_gps_pos[line][last_passed_station]
    station2 = sd.stations_gps_pos[line][last_passed_station + 1]
    delta_lat = float(station2[2]) - float(station1[2])
    delta_lon = float(station2[3]) - float(station1[3])
    return [float(station1[2]) + delta_lat * percentage, float(station1[3]) + delta_lon * percentage]


def save_wt_file(filename, data, simplified_data):
    with open(filename, "w") as f:
        f.write(json.dumps({"data": data, "simplified_data": simplified_data}))


env = simpy.Environment()


for line in sd.lines:
    sd.stations_gps_pos[line] = load_json(line + '.json')

    for i in range(sd.num_vehicles):
        Train(env, i, line, i * sd.delta_schedule)


#for i in range(sd.num_users):

User(env, 0, 0, [sd.milan_lat, sd.milan_lon], [12, 18, "94"])
User(env, 1, 0, [sd.milan_lat - 0.001, sd.milan_lon - 0.01], [5, 10, "94"])
#User(env, 2, 0, [sd.milan_lat - 0.003, sd.milan_lon], [9, 14, "94"])

env.process(save_data_to_file(env))
env.run(until=8000)

#env.process(train(env, 1))
