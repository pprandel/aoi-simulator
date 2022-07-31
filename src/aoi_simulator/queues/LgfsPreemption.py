from numpy import infty
import numpy
from heapq import heappush, heappop
import queueing_tool as qt
from aoi_simulator.queues.AoIQueueServer import AoIQueueServer
from reliability.Distributions import Weibull_Distribution as WB
import json 

"""
Extends QueueServer class from queueing_tool package.
Last Generated First Served (LGFS) Queue with preemption.

Parameters
    ----------
    preemption : int (0: preemption in service, 1: preemption in waiting, 2: preemption conditional)
        Preemption in service: No waiting queue. New arrival replaces agent in service.
        Preemption in waiting: One waiting slot. New arrival replaces agent in waiting queue.
        Preemption conditional: New arrival can preemp in service or in waiting, dinamically
    mrl_file: path to json file with mean residual life function, only for Preemption Conditional (examples in data_aux folder) 
    service_mean: mean value of service function
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class LgfsPreemption(AoIQueueServer):

    def __init__(self, preemption=0, mrl_file=None, service_mean=0, **kwargs):
        super(LgfsPreemption, self).__init__(**kwargs)
        self.preemption = preemption
        self.service_mean = service_mean
        if preemption == 2:
            if mrl_file == None or service_mean==0:
                print("Both mrl_file and service_mean arguments are required for LGFS-C!")
                quit()
        with open(mrl_file, 'r') as f:
            self.MRL = json.load(f)
        self.last_departure_gen_time = 0
        self.contador = 0

    def __repr__(self):
        tmp = ("LcfsPreemption:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)

    # Returns mean residual life for a packet with elapsed service time 't'
    # Approximate to the nearest time 't'
    def expected_sv(self, t):
            return self.MRL.get(t, self.MRL[min(self.MRL.keys(), key=lambda k: abs(float(k)-t))])

    def next_event(self):
        
        if self._departures[0]._time < self._arrivals[0]._time:
            new_depart = heappop(self._departures)
            self.last_departure_gen_time = new_depart.gen_time
            self._current_t = new_depart._time
            self._num_total -= 1
            self.num_system -= 1
            self.num_departures += 1
            new_depart.queue_action(self, 2)

            if self.collect_data and new_depart.agent_id in self.data:
                self.data[new_depart.agent_id][-1][2] = self._current_t

            # Preemption in waiting or conditional
            if len(self.queue) > 0:
                agent = self.queue.popleft()
                if self.collect_data and agent.agent_id in self.data:
                    self.data[agent.agent_id][-1][1] = self._current_t
                agent._time = self.service_f(self._current_t)
                agent.queue_action(self, 1)
                heappush(self._departures, agent)

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
                        [[arrival._time, 0, 0, 0, self.num_system]]
                else:
                    self.data[arrival.agent_id]\
                        .append([arrival._time, 0, 0, 0, self.num_system])

            arrival.queue_action(self, 0)

            # Preemption in service
            if self.preemption == 0:
                # No agent in service
                if self.num_system == 1:
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                    # Go directly to service
                    heappush(self._departures, arrival)
                    arrival.queue_action(self, 1)
                    arrival._time = self.service_f(arrival._time)

                # Agent already in service is replaced if new arrival is fresher
                else:
                    agent_in_sv = self._departures[0]
                    if arrival.gen_time > agent_in_sv.gen_time:
                        # Remove agent in service
                        agent_replaced = heappop(self._departures)
                        # Include new agent in service
                        heappush(self._departures, arrival)
                        if self.collect_data:
                            self.data[arrival.agent_id][-1][1] = arrival._time
                            self.data[agent_replaced.agent_id][-1][1] = 0
                        arrival.queue_action(self, 1)
                        arrival._time = self.service_f(arrival._time)
                    self.num_system -= 1
                self._update_time()
            
            # Preemption in waiting
            elif self.preemption == 1:
                # No agent in service / waiting
                if self.num_system == 1:
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                    # Go directly to service
                    heappush(self._departures, arrival)
                    arrival.queue_action(self, 1)
                    arrival._time = self.service_f(arrival._time)

                # One agent in service
                elif self.num_system == 2:
                    self.queue.append(arrival)
                    if len(self.queue) > 1:
                        print("Error: queue can't be bigger than 1 !")

                # One agent in service and one agent in waiting
                else:
                    agent_in_queue = self.queue[0]
                    if arrival.gen_time > agent_in_queue.gen_time:
                        # Remove agent in waiting
                        agent_replaced = self.queue.popleft()
                        # Include new arrival in waiting
                        self.queue.append(arrival)             
                    self.num_system -= 1
                self._update_time()

            # Preemption conditional
            elif self.preemption == 2:
                # No agent in service
                if self.num_system == 1:
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                    # Go directly to service
                    heappush(self._departures, arrival)
                    arrival.queue_action(self, 1)
                    arrival._time = self.service_f(arrival._time)
                # One agent in service
                elif self.num_system == 2:
                    agent_in_sv = self._departures[0]
                    if arrival.gen_time > agent_in_sv.gen_time:
                        # New agent is fresher
                        s0 = self.last_departure_gen_time
                        s1 = agent_in_sv.gen_time
                        s2 = arrival.gen_time
                        MRL = self.expected_sv(self._current_t - self.data[agent_in_sv.agent_id][-1][1])
                        if ((s1 - s0)*self.service_mean) < ((s2 - s0)*MRL):
                        # Remove agent in service  
                            agent_replaced = heappop(self._departures)
                            self.num_system -= 1
                            # Include new agent in service
                            heappush(self._departures, arrival)
                            if self.collect_data:
                                self.data[arrival.agent_id][-1][1] = arrival._time
                                self.data[agent_replaced.agent_id][-1][1] = 0
                            arrival.queue_action(self, 1)
                            arrival._time = self.service_f(arrival._time)
                        else:
                        # New arrival is queued
                            self.queue.append(arrival)             
                            self.contador += 1    
                    else:
                        self.num_system -= 1
                # One agent in service and one agent in waiting     
                else:    
                    agent_in_queue = self.queue[0]
                    agent_in_sv = self._departures[0]
                    if arrival.gen_time > agent_in_queue.gen_time:
                        # Remove agent in queue (obsolete)
                        agent_replaced = self.queue.popleft()
                        s0 = self.last_departure_gen_time
                        s1 = agent_in_sv.gen_time
                        s2 = arrival.gen_time
                        MRL = self.expected_sv(self._current_t - self.data[agent_in_sv.agent_id][-1][1])
                        if ((s1 - s0)*self.service_mean) < ((s2 - s0)*MRL):
                        # Remove agent in service  
                            agent_replaced = heappop(self._departures)
                            self.num_system -= 1
                            # Include new agent in service
                            heappush(self._departures, arrival)
                            if self.collect_data:
                                self.data[arrival.agent_id][-1][1] = arrival._time
                                self.data[agent_replaced.agent_id][-1][1] = 0
                            arrival.queue_action(self, 1)
                            arrival._time = self.service_f(arrival._time)
                        else:
                        # New arrival is queued
                            self.queue.append(arrival)             
                            self.contador += 1   
                    self.num_system -= 1
                self._update_time()