import shared_data as sd


class Train(object):

    delta_t = 1
    last_station = -1
    train_id = 0
    line = 0
    starting_time = 0

    def __init__(self, env, train_id, line, starting_time):
        self.env = env
        self.action = env.process(self.run())
        self.train_id = train_id
        self.starting_time = starting_time
        self.line = line

    def run(self):

        # yield self.env.process(self.init_train())

        sd.vehicles_pos_array[self.line][self.train_id] = - self.starting_time * sd.starting_speed
        # print (sd.vehicles_pos_array[line][self.train_id])

        # yield self.env.process(self.stop_at_station())

        while self.last_station < sd.n_stations[self.line] - 1:

            if sd.vehicles_pos_array[self.line][self.train_id] < 0:
                sd.vehicles_pos_array[self.line][self.train_id] += sd.starting_speed * self.delta_t
            else:
                segment = sd.vehicles_pos_array[self.line][self.train_id] // sd.segment_length
                speed = sd.speed_d if segment % 2 else sd.speed_p
                sd.vehicles_pos_array[self.line][self.train_id] += speed * self.delta_t

                # print("time: " + str(self.env.now // 60) + " min - " + str(self.train_id) + " DEPARTING")

            if sd.vehicles_pos_array[self.line][self.train_id] >= (self.last_station + 1) * sd.segment_length:
                yield self.env.process(self.stop_at_station(sd.station_stop))
            else:
                yield self.env.timeout(self.delta_t)

        print("time: " + str(self.env.now // 60) + " min - " + str(self.train_id) +" ARRIVED TO DESTINATION")
        # remove train from last station
        sd.vehicles_pos_array[self.line][self.train_id] += 1

        sd.arrived_vehicles[self.line] += 1

    def stop_at_station(self, station_stop):
        self.last_station += 1
        print("time: " + str(round(self.env.now / 60)) + " min - " + str(self.train_id) +' arrived at station ' + str(self.last_station))
        sd.vehicles_pos_array[self.line][self.train_id] = self.last_station * sd.segment_length
        print(".......  ", station_stop)
        yield self.env.timeout(station_stop)
