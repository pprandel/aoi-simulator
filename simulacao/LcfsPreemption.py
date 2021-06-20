from numpy import infty
import numpy
from heapq import heappush, heappop
import queueing_tool as qt

"""
Extends QueueServer Class from queueing_tool package
Last Come First Served Queue with finite capacity and preemption

Parameters
    ----------
    preemption : int (0: preemption in service, 1: preemption in waiting)
        Preemption in service: No waiting queue. New arrival replaces agent in service.
        Preemption in waiting: One waiting slot. New arrival replaces agent in waiting queue.
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class LcfsPreemption(qt.QueueServer):

    def __init__(self, preemption=0, **kwargs):
        super(LcfsPreemption, self).__init__(**kwargs)
        self.preemption = preemption

    def __repr__(self):
        tmp = ("LcfsPreemption:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)

    def next_event(self):
        
        # Preemption in service
        if self.preemption == 0:

            if self._departures[0]._time < self._arrivals[0]._time:
                new_depart = heappop(self._departures)
                self._current_t = new_depart._time
                self._num_total -= 1
                self.num_system -= 1
                self.num_departures += 1

                if self.collect_data and new_depart.agent_id in self.data:
                    self.data[new_depart.agent_id][-1][2] = self._current_t

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
                            [[arrival._time, 0, 0, 0, self.num_system]]
                    else:
                        self.data[arrival.agent_id]\
                            .append([arrival._time, 0, 0, 0, self.num_system])

                arrival.queue_action(self, 0)

                # No agent in service
                if self.num_system == 1:
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                    heappush(self._departures, arrival)
                # Agent already in service is replaced
                else:
                    agent_replaced = heappop(self._departures)
                    self.num_system -= 1
                    heappush(self._departures, arrival)
                    if self.collect_data:
                        self.data[arrival.agent_id][-1][1] = arrival._time
                        self.data[agent_replaced.agent_id][-1][1] = 0

                arrival.queue_action(self, 1)
                arrival._time = self.service_f(arrival._time)
                self._update_time()