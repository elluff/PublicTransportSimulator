starting_speed = 1  # m/s

arrived_vehicles = 0

stations_gps_pos = []

milan_lat = 45.4638768
milan_lon = 9.1905701

speed_p = 1.5  # m/s
speed_d = 2.5  # m/s

station_stop = 30
station_incr = 0

n_stations = 20
segment_length = 500  # meters
delta_schedule = 60 * 10  # schedule


num_vehicles = 15  # number of vehicles on a line
num_users = 20  # number of users walking or riding a vehicle


vehicles_pos_array = [-1000 for _ in range(num_vehicles)]
users_pos_array = [[milan_lat, milan_lon, 10, 15, None] for _ in range(num_users)] # [lat, lon, start_station, end_station, line]


gps_trains_position = []
gps_users_position = []

