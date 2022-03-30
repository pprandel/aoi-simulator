from numpy import infty
from heapq import heappush, heappop
from aoi_simulator.AoIQueueServer import AoIQueueServer

"""
Extends QueueServer Class from queueing_tool package
Last Generated First Served Queue with no preemption allowed
LGFS: Last generated packet is served first among all packets in queue
MAX-LGFS: Last generated packet from the source with the maximum age is served first among all packets in queue
MASIF-LGFS: Last generated packet from the source with the maximum Age of Served Information (AoSI) is served first among all packets in queue
Reference: @misc{sun2018ageoptimal,
            title={Age-Optimal Updates of Multiple Information Flows}, 
            author={Yin Sun and Elif Uysal-Biyikoglu and Sastry Kompella},
            year={2018},
            eprint={1801.02394},
            archivePrefix={arXiv},
            primaryClass={cs.IT}
        }
Parameters
    ----------
    policy : int [0: LGFS (Last generated First Served), 1: MAX-LGFS (Maximum Age First), 2: MASIF-LGFS (Maximum Age of Served Information First)]
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class LgfsMultiServerNoPreemption2(AoIQueueServer):

    def __init__(self, **kwargs):
        super(LgfsMultiServerNoPreemption2, self).__init__(**kwargs)
        # Dic with source index as keys and last departure generation time as values
        self._last_departures_gen_time = {"freshest": infty}
        # We define a queue as a dic with a key to each source
        self.multi_queue = {}

    def __repr__(self):
        tmp = ("LgfsMultiServerNoPreemption:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
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
            # Max aged source in queue
            oldest_source = "freshest"
            for source, agent in self.multi_queue.items():
                # Source is already in service
                if check_source_service(source):
                    continue
                if self.get_last_departures_gen_time(source) < self.get_last_departures_gen_time(oldest_source):
                    oldest_source = source
                    agent_served = agent
            del self.multi_queue[source]
            return agent_served

        # # #

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

            # Fetch next agent according to the policy
            if bool(self.multi_queue):
                agent = fetch_queue()
                if self.collect_data and agent.agent_id in self.data:
                    self.data[agent.agent_id][-1][1] = self._current_t
                # Update in service time of agent
                self.set_in_service_gen_time(agent.agent_id[0], agent.gen_time)
                agent._time = self.service_f(self._current_t)
                agent.queue_action(self, 1)
                heappush(self._departures, agent)

            new_depart.queue_action(self, 2)
            self._update_time()
            return new_depart

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
            # We always enqueue new arrivals
            self.enqueue(arrival)

            self._update_time()