from numpy import infty
from heapq import heappush, heappop
from AoIQueueServer import AoIQueueServer

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

class LgfsMultiServerNoPreemption(AoIQueueServer):

    def __init__(self, policy=0, **kwargs):
        super(LgfsMultiServerNoPreemption, self).__init__(**kwargs)
        self.policy = policy
        # Dic with source index as keys and last departure generation time as values
        self._last_departures_gen_time = {"oldest": infty}
        # Dic with source index as keys and last in service agent generation time as values
        self._in_service_gen_time = {"oldest": infty}

    def __repr__(self):
        tmp = ("LgfsMultiServerNoPreemption:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)

    # Getters and setters
    def get_last_departures_gen_time(self, source):
        if source in self._last_departures_gen_time:
            return self._last_departures_gen_time[source]
        else:
            return 0

    def get_in_service_gen_time(self, source):
        if source in self._in_service_gen_time:
            return self._in_service_gen_time[source]
        else:
            return 0

    def set_last_departures_gen_time(self, source, time):
        if source in self._last_departures_gen_time:
            if time < self._last_departures_gen_time[source]:
                return
        self._last_departures_gen_time[source] = time

    def set_in_service_gen_time(self, source, time):
        if source in self._in_service_gen_time:
            if time < self._in_service_gen_time[source]:
                return
        self._in_service_gen_time[source] = time

    # # #
    
    def next_event(self):
    
        # Return next agent to be served
        def fetch_queue():
            agent_served = None

            # LGFS
            if self.policy == 0:
                newest_gen_time = 0
                # Get newest agent from all sources
                for agent in self.queue:
                    if repr(agent) == 'InftyAgent':
                        continue
                    if agent.gen_time > newest_gen_time:
                        newest_gen_time = agent.gen_time
                        agent_served = agent

            # MAX-LGFS
            elif self.policy == 1: 
                # Max age source
                oldest_source = "oldest"
                # Newest gen time from max age source
                newest_gen_time = 0
                for agent in self.queue:
                    if repr(agent) == 'InftyAgent':
                        continue
                    agent_source = agent.agent_id[0]
                    # If agents have same source, we choose the newest generated time
                    if agent_source == oldest_source:
                        if agent.gen_time > newest_gen_time:
                            agent_served = agent
                            newest_gen_time = agent.gen_time
                    elif self.get_last_departures_gen_time(agent_source) < self.get_last_departures_gen_time(oldest_source):
                        oldest_source = agent_source
                        newest_gen_time = agent.gen_time
                        agent_served = agent

            # MASIF-LGFS
            else:
                # Max age source
                oldest_source = "oldest"
                # Newest gen time from max age source
                newest_gen_time = 0
                for agent in self.queue:
                    if repr(agent) == 'InftyAgent':
                        continue
                    agent_source = agent.agent_id[0]
                    # If agents have same source, we choose the newest generated time
                    if agent_source == oldest_source:
                        if agent.gen_time > newest_gen_time:
                            agent_served = agent
                            newest_gen_time = agent.gen_time
                    elif self.get_in_service_gen_time(agent_source) < self.get_in_service_gen_time(oldest_source):
                        oldest_source = agent_source
                        newest_gen_time = agent.gen_time
                        agent_served = agent

            self.queue.remove(agent_served)
            return agent_served

        # # #

        def remove_obsolete():
            pass

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

            remove_obsolete()

            # Fetch next agent according to the policy
            if len(self.queue) > 0:
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
                
            # All servers busy: agent is queued
            else:
                self.queue.append(arrival)

            self._update_time()