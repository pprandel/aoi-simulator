from numpy import infty
from heapq import heappush, heappop
from aoi_simulator.AoIQueueServer import AoIQueueServer

"""
Extends QueueServer Class from queueing_tool package
Last Generated First Served Queue with preemption under different policies
LGFS: Last generated packet is served first (among all sources)
MAX-LGFS: Last generated packet from the source with the maximum age is served first
MASIF-LGFS: Last generated packet from the source with the maximum Age of Served Information (AoSI) is served first
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

class LgfsMultiServerPreemption(AoIQueueServer):

    def __init__(self, policy=0, **kwargs):
        super(LgfsMultiServerPreemption, self).__init__(**kwargs)
        self.policy = policy
        # Dic with source index as keys and last departure generation time as values
        self._last_departures_gen_time = {"freshest": 0}
        # We define a queue as a dic with a key to each source
        self.multi_queue = {}

    def __repr__(self):
        tmp = ("LgfsMultiServerPreemption:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
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

    def dequeue(self,source):
        if source in self.multi_queue.keys():
            return self.multi_queue[source]
        else:
            return None

    # Getters and setters
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


            # if len(self.queue) > 0:
            #     agent = self.queue.popleft()
            #     if self.collect_data and agent.agent_id in self.data:
            #         self.data[agent.agent_id][-1][1] = self._current_t

            #     agent._time = self.service_f(self._current_t)
            #     agent.queue_action(self, 1)
            #     heappush(self._departures, agent)

            new_depart.queue_action(self, 2)
            self._update_time()
            return new_depart

        elif self._arrivals[0]._time < infty:
            arrival = heappop(self._arrivals)
            self._current_t = arrival._time
            arrival_source = arrival.agent_id[0]

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

            # We have idle server(s)
            if self.num_system <= self.num_servers:
                if self.collect_data:
                    self.data[arrival.agent_id][-1][1] = arrival._time
                # Update in service time
                self.set_in_service_gen_time(arrival_source, arrival.gen_time)
                arrival._time = self.service_f(arrival._time)
                arrival.queue_action(self, 1)
                heappush(self._departures, arrival)
                
            # Agent already in service is replaced
            else:
                agent_replaced = None

                # LGFS
                if self.policy == 0:
                    oldest_gen_time = infty
                    # Get oldest agent from all sources
                    for agent in self._departures:
                        if repr(agent) == 'InftyAgent':
                            continue
                        if agent.gen_time < oldest_gen_time:
                            oldest_gen_time = agent.gen_time
                            agent_replaced = agent
                    # Check if the last arrival is older
                    if arrival.gen_time < agent_replaced.gen_time:
                        agent_replaced = None

                # MAX-LGFS
                elif self.policy == 1: 
                    # Freshest source will be replaced (prioritize oldest sources)
                    freshest_source = "freshest"
                    # Oldest gen time from max age source
                    oldest_gen_time = infty
                    for agent in self._departures:
                        if repr(agent) == 'InftyAgent':
                            continue
                        agent_source = agent.agent_id[0]
                        # If agents have same source, we choose the oldest generated time
                        if agent_source == freshest_source:
                            if agent.gen_time < oldest_gen_time:
                                agent_replaced = agent
                                oldest_gen_time = agent.gen_time
                        elif self.get_last_departures_gen_time(agent_source) > self.get_last_departures_gen_time(freshest_source):
                            freshest_source = agent_source
                            oldest_gen_time = agent.gen_time
                            agent_replaced = agent
                        
                    # Check if the last arrival is older
                    if arrival_source == freshest_source:
                        if arrival.gen_time < oldest_gen_time:
                                agent_replaced = None
                    elif self.get_last_departures_gen_time(arrival_source) > self.get_last_departures_gen_time(freshest_source):
                        agent_replaced = None

                # MASIF-LGFS
                else:
                    # Max age source
                    freshest_source = "freshest"
                    # Oldest gen time from max age source
                    oldest_gen_time = infty
                    for agent in self._departures:
                        if repr(agent) == 'InftyAgent':
                            continue
                        agent_source = agent.agent_id[0]
                        # If agents have same source, we choose the oldest generated time
                        if agent_source == freshest_source:
                            if agent.gen_time < oldest_gen_time:
                                agent_replaced = agent
                                oldest_gen_time = agent.gen_time
                        elif self.get_in_service_gen_time(agent_source) > self.get_in_service_gen_time(freshest_source):
                            freshest_source = agent_source
                            oldest_gen_time = agent.gen_time
                            agent_replaced = agent
                        
                    # Check if the last arrival is older
                    if arrival_source == freshest_source:
                        if arrival.gen_time < oldest_gen_time:
                                agent_replaced = None
                    elif self.get_in_service_gen_time(arrival_source) > self.get_in_service_gen_time(freshest_source):
                        agent_replaced = None

                if agent_replaced is not None:
                    # Remove the selected agent in service
                    self._departures.remove(agent_replaced)
                    # Update in_service_gen_time_list
                    self.remove_in_service_gen_time(agent_replaced.agent_id[0], agent_replaced.gen_time)
                    # Update num_system
                    self.num_system -= 1

                    # Include new agent in service
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                        self.data[agent_replaced.agent_id][-1][1] = 0
                    # Update in service last gen time
                    self.set_in_service_gen_time(arrival_source, arrival.gen_time)
                    arrival._time = self.service_f(arrival._time)
                    heappush(self._departures, arrival)
                else:
                    self.num_system -= 1
            self._update_time()
        
       