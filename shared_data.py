starting_speed = 1  # m/s


milan_lat = 45.4638768
milan_lon = 9.1905701

speed_p = 1.5  # m/s
speed_d = 2.5  # m/s

station_stop = 30
station_incr = 0

segment_length = 500  # meters
delta_schedule = 60 * 10  # schedule


num_vehicles = 15  # number of vehicles on a line
num_users = 20  # number of users walking or riding a vehicle


lines = ["15", "94", "61"]

arrived_vehicles = {}
vehicles_pos_array = {}
gps_trains_position = {}
stations_gps_pos = {}
n_stations = {}
n_stations["15"] = 27
n_stations["61"] = 41
n_stations["94"] = 22


for line in lines:
    vehicles_pos_array[line] = [-1000 for _ in range(num_vehicles)]
    gps_trains_position[line] = []
    stations_gps_pos[line] = []
    arrived_vehicles[line] = 0


users_pos_array = [[-1, -1, -1, -1, None] for _ in range(num_users)] # [lat, lon, start_station, end_station, line]
gps_users_position = []
