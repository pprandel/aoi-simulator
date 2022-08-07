from numpy import infty
from heapq import heappush, heappop
from aoi_simulator.queues.AoIQueueServer import AoIQueueServer

"""
Extends QueueServer Class from queueing_tool package
Multi source and multi server model
Last Generated First Served Queue - Multi Preemption in Waiting
LGFS: Last generated packet is served first among all packets in queue
Multi Preemption in Waiting: Each source has a waiting queue, where preemption is allowed
Reference: not published yet...
Parameters
    ----------
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class LgfsMultiServerPreemptionW(AoIQueueServer):

    def __init__(self, **kwargs):
        super(LgfsMultiServerPreemptionW, self).__init__(**kwargs)
        # Dic with source index as keys and last departure generation time as values
        self._last_departures_gen_time = {"freshest": infty}
        # We define a queue as a dic with a key to each source
        self.multi_queue = {}

    def __repr__(self):
        tmp = ("LgfsMultiServerPreemptionW:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)


    def enqueue(self, agent):
        source = agent.agent_id[0]
        if source in self.multi_queue.keys():
            gen_time = agent.gen_time
            if gen_time > self.multi_queue[source].gen_time:
                self.multi_queue[source] = agent
            self.num_system -= 1
        else:
            self.multi_queue[source] = agent

    # Getters and setters for last_departures
    def get_last_departures_gen_time(self, source):
        if source in self._last_departures_gen_time:
            return self._last_departures_gen_time[source]
        else:
            return 0

    def set_last_departures_gen_time(self, source, time):
        if source in self._last_departures_gen_time:
            if time < self._last_departures_gen_time[source]:
                return
        self._last_departures_gen_time[source] = time

    # # #
    
    def next_event(self):
    
        # Check if source has an agent in service
        def check_source_service(source):
            for agent in self._departures:
                if repr(agent) == 'InftyAgent':
                    continue
                if agent.agent_id[0] == source:
                    return True
            return False

        # # #

        # Return next agent to be served
        def fetch_queue():
            agent_served = None
            source_served = None
            # Max aged source in queue
            oldest_source = "freshest"
            for source, agent in self.multi_queue.items():
                # Source is already in service
                if check_source_service(source):
                    continue
                if self.get_last_departures_gen_time(source) < self.get_last_departures_gen_time(oldest_source):
                    oldest_source = source
                    agent_served = agent
                    source_served = source
            if agent_served:
                del self.multi_queue[source_served]
            return agent_served

        # # #

        # Departure
        if self._departures[0]._time < self._arrivals[0]._time:
            new_depart = heappop(self._departures)
            self._current_t = new_depart._time
            self._num_total -= 1
            self.num_system -= 1
            self.num_departures += 1
            new_depart_source = new_depart.agent_id[0]
            # Update last departure time
            self.set_last_departures_gen_time(new_depart_source, new_depart.gen_time)

            if self.collect_data and new_depart.agent_id in self.data:
                self.data[new_depart.agent_id][-1][2] = self._current_t

            # There is at least one packet in the queue
            if bool(self.multi_queue):
                agent = fetch_queue()
                if agent is not None:
                    if self.collect_data and agent.agent_id in self.data:
                        self.data[agent.agent_id][-1][1] = self._current_t
                    agent._time = self.service_f(self._current_t)
                    agent.queue_action(self, 1)
                    heappush(self._departures, agent)

            new_depart.queue_action(self, 2)
            self._update_time()
            return new_depart

        # Arrival
        elif self._arrivals[0]._time < infty:
            arrival = heappop(self._arrivals)
            self._current_t = arrival._time

            if self._active:
                self._add_arrival()

            self.num_system += 1
            self._num_arrivals += 1

            if self.collect_data:
                b = 0 if self.num_system <= self.num_servers else 1
                if arrival.agent_id not in self.data:
                    self.data[arrival.agent_id] = \
                        [[arrival._time, 0, 0, len(self.queue) + b, self.num_system]]
                else:
                    self.data[arrival.agent_id]\
                        .append([arrival._time, 0, 0, len(self.queue) + b, self.num_system])
            arrival.queue_action(self, 0)

            # Arrival source already in service
            # TBC

            # We have idle server(s)
            if len(self._departures) <= self.num_servers:
                if self.collect_data:
                    self.data[arrival.agent_id][-1][1] = arrival._time
                arrival._time = self.service_f(arrival._time)
                arrival.queue_action(self, 1)
                heappush(self._departures, arrival)
            else:
                self.enqueue(arrival)

            self._update_time()