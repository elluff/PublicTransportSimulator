import shared_data as sd
from random import gauss
from geopy.distance import vincenty

stationDistanceError = 50

class User(object):

    delta_t = 1
    user_id = 0
    starting_time = 0

    walking_speed = 0.00001


    def __init__(self, env, user_id, starting_time):
        self.env = env
        self.action = env.process(self.run())
        self.user_id = user_id
        self.starting_time = starting_time

        self.walking = True
        self.arrived = False

    def run(self):

        # sd.users_pos_array[self.user_id] = [-1, -1]

        print sd.stations_gps_pos
        line = sd.users_pos_array[self.user_id][4]
        start_st = sd.stations_gps_pos[sd.users_pos_array[self.user_id][2]]
        start_st[2] = float(start_st[2])
        start_st[3] = float(start_st[3])

        end_st = sd.stations_gps_pos[sd.users_pos_array[self.user_id][3]]
        end_st[2] = float(end_st[2])
        end_st[3] = float(end_st[3])

        while True:

            if closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], start_st[2], start_st[3]) and closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], sd.gps_trains_position[-1][0][0], sd.gps_trains_position[-1][0][1]):
                self.walking = False

            if closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], end_st[2], end_st[3]):
                self.walking = True
                self.arrived = True

 
            if not self.walking:
                print "onBoard"
                coordinates = generateUsersGpsPos(sd.gps_trains_position)
                sd.users_pos_array[self.user_id][0] = coordinates[0]
                sd.users_pos_array[self.user_id][1] = coordinates[1]
            elif self.arrived:
                print "arrived"
                sd.users_pos_array[self.user_id][0] += self.walking_speed
                sd.users_pos_array[self.user_id][1] += self.walking_speed
            else:
                print "moving to station"

                if (sd.users_pos_array[self.user_id][0] > start_st[2]):
                    sd.users_pos_array[self.user_id][0] -= self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][0] += self.walking_speed

                if (sd.users_pos_array[self.user_id][1] > start_st[3]):
                    sd.users_pos_array[self.user_id][1] -= self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][1] += self.walking_speed


            yield self.env.timeout(self.delta_t)


def closeToStation(usr_lat, usr_lon, stat_lat, stat_lon):
    dist = vincenty((usr_lat, usr_lon), (stat_lat, stat_lon)).meters
    print dist
    return dist <= stationDistanceError


def generateUsersGpsPos(trains):
    if not len(trains):
        return [-1, -1]
    first_train = trains[-1][0]
    return [gauss(float(first_train[0]), 0.0005), gauss(float(first_train[1]), 0.0005)]

