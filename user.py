import shared_data as sd
from random import gauss
from geopy.distance import vincenty

stationDistanceError = 20

GPSnoise = 0.00025
#GPSnoise = 0

class User(object):

    delta_t = 1
    user_id = 0
    starting_time = 0
    starting_pos = None
    line = None

    walking_speed = 0.00001

    def __init__(self, env, user_id, starting_time, starting_pos, line):
        self.env = env
        self.action = env.process(self.run())
        self.user_id = user_id
        self.starting_time = starting_time
        self.starting_pos = starting_pos
        self.line = line
        self.train_id = None

        self.walking = True
        self.arrived = False

    def run(self):

        # sd.users_pos_array[self.user_id] = [-1, -1]

        sd.users_pos_array[self.user_id][0] = self.starting_pos[0]
        sd.users_pos_array[self.user_id][1] = self.starting_pos[1]

        sd.users_pos_array[self.user_id][2] = self.line[0]
        sd.users_pos_array[self.user_id][3] = self.line[1]
        sd.users_pos_array[self.user_id][4] = self.line[2]

        self.line = sd.users_pos_array[self.user_id][4]
        start_st = sd.stations_gps_pos[self.line][sd.users_pos_array[self.user_id][2]]
        start_st[2] = float(start_st[2])
        start_st[3] = float(start_st[3])

        end_st = sd.stations_gps_pos[self.line][sd.users_pos_array[self.user_id][3]]
        end_st[2] = float(end_st[2])
        end_st[3] = float(end_st[3])

        while True:

            if self.walking and len(sd.gps_trains_position[self.line]) is not 0:
                for i in range(len(sd.gps_trains_position[self.line][-1])):
                    train_on_line = sd.gps_trains_position[self.line][-1][i]
                    if closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], start_st[2], start_st[3]) and closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], train_on_line[0], train_on_line[1]):
                        self.walking = False
                        self.train_id = i

            if closeToStation(sd.users_pos_array[self.user_id][0], sd.users_pos_array[self.user_id][1], end_st[2], end_st[3]):
                self.walking = True
                self.arrived = True

            if not self.walking:
                coordinates = generateUsersGpsPos(sd.gps_trains_position[self.line], self.train_id)
                sd.users_pos_array[self.user_id][0] = coordinates[0]
                sd.users_pos_array[self.user_id][1] = coordinates[1]
            elif self.arrived:
                # print "arrived"
                if sd.users_pos_array[self.user_id][0] > sd.milan_lat:
                    sd.users_pos_array[self.user_id][0] += 5 * self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][0] -= 5 * self.walking_speed

                if sd.users_pos_array[self.user_id][1] > sd.milan_lon:
                    sd.users_pos_array[self.user_id][1] += 5 * self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][1] -= 5 * self.walking_speed

            else:
                # print "moving to station"

                if (sd.users_pos_array[self.user_id][0] > start_st[2]):
                    sd.users_pos_array[self.user_id][0] -= self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][0] += self.walking_speed

                if (sd.users_pos_array[self.user_id][1] > start_st[3]):
                    sd.users_pos_array[self.user_id][1] -= self.walking_speed
                else:
                    sd.users_pos_array[self.user_id][1] += self.walking_speed

                # print "--------------"
                # print sd.users_pos_array[self.user_id][0]
                sd.users_pos_array[self.user_id][0] = gauss(float(sd.users_pos_array[self.user_id][0]), GPSnoise / 10)
                # print sd.users_pos_array[self.user_id][0]
                sd.users_pos_array[self.user_id][1] = gauss(sd.users_pos_array[self.user_id][1], GPSnoise / 10)

            yield self.env.timeout(self.delta_t)


def closeToStation(usr_lat, usr_lon, stat_lat, stat_lon):
    dist = vincenty((usr_lat, usr_lon), (stat_lat, stat_lon)).meters
    return dist <= stationDistanceError


def generateUsersGpsPos(trains, train_id):
    if not len(trains):
        return [-1, -1]

    selected_train = trains[-1][train_id]
    return [gauss(float(selected_train[0]), GPSnoise), gauss(float(selected_train[1]), GPSnoise)]

