import shared_data


class Train(object):

    delta_t = 1
    last_station = -1
    train_id = 0

    starting_time = 0

    def __init__(self, env, train_id, starting_time):
        self.env = env
        self.action = env.process(self.run())
        self.train_id = train_id
        self.starting_time = starting_time

    def run(self):

        #yield self.env.process(self.init_train())

        shared_data.vehicles_pos_array[self.train_id] = - self.starting_time * shared_data.starting_speed
        print (shared_data.vehicles_pos_array[self.train_id])

    #    yield self.env.process(self.stop_at_station())

        while self.last_station < shared_data.n_stations - 1:

            if shared_data.vehicles_pos_array[self.train_id] < 0:
                shared_data.vehicles_pos_array[self.train_id] += shared_data.starting_speed * self.delta_t
            else:
                segment = shared_data.vehicles_pos_array[self.train_id] // shared_data.segment_length
                speed = shared_data.speed_d if segment % 2 else shared_data.speed_p
                shared_data.vehicles_pos_array[self.train_id] += speed * self.delta_t

              #  print("time: " + str(self.env.now // 60) + " min - " + str(self.train_id) + " DEPARTING")

            if shared_data.vehicles_pos_array[self.train_id] >= (self.last_station + 1) * shared_data.segment_length:
                yield self.env.process(self.stop_at_station(shared_data.station_stop))
            else:
                yield self.env.timeout(self.delta_t)

        print("time: "+str(self.env.now//60) + " min - " + str(self.train_id) +" ARRIVED TO DESTINATION")
        #remove train from last station
        shared_data.vehicles_pos_array[self.train_id] += 1
        
        shared_data.arrived_vehicles += 1

  #  def init_train(self):
#        vehicles_pos_array[self.train_id] = - self.starting_time * starting_speed

#        while (self.env.now < starting_time):
  #          vehicles_pos_array[self.train_id] = 0

   #         yield self.env.timeout(self.delta_t)

    #    vehicles_pos_array[self.train_id] = 0

    def stop_at_station(self, station_stop):
        self.last_station += 1
        print("time: "+str(round(self.env.now / 60)) + " min - " + str(self.train_id) +' arrived at station ' + str(self.last_station))
        shared_data.vehicles_pos_array[self.train_id] = self.last_station * shared_data.segment_length
        print(".......  ", station_stop)
        yield self.env.timeout(station_stop)

