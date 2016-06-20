import simpy

speed = 5 #m/s
segment_length = 500 #meters
delta_schedule = 60 * 5 #schedule

class Train(object):

    station_stop = 60
    delta_t = 1
    n_stations = 20
    train_pos = 0
    last_station = 0
    train_id = 0

    starting_time = 0

    def __init__(self, env, train_id, starting_time):
        self.env = env
        self.action = env.process(self.run())
        self.train_id = train_id
        self.starting_time = starting_time

    def run(self):

        yield self.env.timeout(self.starting_time)
        print("time: "+str(self.env.now//60) + " min - " + str(self.train_id) + " DEPARTING")
        while self.last_station < self.n_stations:
            self.train_pos += speed * self.delta_t

            if self.train_pos >= (self.last_station + 1) * segment_length:
                yield self.env.process(self.stop_at_station(self.station_stop))
            else:
                #print("moving to station "+str(self.last_station+1)+" (pos: "+str(self.train_pos)+")")
                yield self.env.timeout(self.delta_t)

        print("time: "+str(self.env.now//60) + " min - " + str(self.train_id) + " ARRIVED TO DESTINATION")

    def stop_at_station(self, station_stop):
        print("time: "+str(self.env.now//60) + " min - " + str(self.train_id) + ' arrived at station ' + str(self.last_station))
        self.last_station += 1
        self.train_pos = self.last_station * segment_length
        yield self.env.timeout(station_stop)

env = simpy.Environment()
for i in range(4):
    Train(env, i, i * delta_schedule)
env.run()

#env.process(train(env, 1))
