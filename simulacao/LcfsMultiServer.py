from numpy import infty
import numpy
from heapq import heappush, heappop
import queueing_tool as qt

"""
Extends QueueServer Class from queueing_tool package
Last generated First Come First Served Queue with multiple servers
When all servers are busy, a new arrival replaces the oldest agent already in service
Parameters
    ----------
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class LcfsMultiServer(qt.QueueServer):

    def __init__(self, preemption=0, **kwargs):
        super(LcfsMultiServer, self).__init__(**kwargs)

    def __repr__(self):
        tmp = ("LcfsMultiServer:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)

    def next_event(self):
        """Simulates the queue forward one event.

        Use :meth:`.simulate` instead.

        Returns
        -------
        out : :class:`.Agent` (sometimes)
            If the next event is a departure then the departing agent
            is returned, otherwise nothing is returned.

        See Also
        --------
        :meth:`.simulate` : Simulates the queue forward.
        """
        if self._departures[0]._time < self._arrivals[0]._time:
            new_depart = heappop(self._departures)
            self._current_t = new_depart._time
            self._num_total -= 1
            self.num_system -= 1
            self.num_departures += 1

            if self.collect_data and new_depart.agent_id in self.data:
                self.data[new_depart.agent_id][-1][2] = self._current_t

            if len(self.queue) > 0:
                agent = self.queue.popleft()
                if self.collect_data and agent.agent_id in self.data:
                    self.data[agent.agent_id][-1][1] = self._current_t

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

            if self.num_system <= self.num_servers:
                if self.collect_data:
                    self.data[arrival.agent_id][-1][1] = arrival._time

                arrival._time = self.service_f(arrival._time)
                arrival.queue_action(self, 1)
                heappush(self._departures, arrival)
            # Agent already in service is replaced
            else:
                for agent in self.num_departures:
                    ################### PAREI AQUI!
                    self.data[agent.agent_id]
                # Remove agent in service
                agent_replaced = heappop(self._departures)
                self.num_system -= 1
                # Include new agent in service
                heappush(self._departures, arrival)
                if self.collect_data:
                    self.data[arrival.agent_id][-1][1] = arrival._time
                    self.data[agent_replaced.agent_id][-1][1] = 0

            self._update_time()
        
       