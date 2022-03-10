import queueing_tool as qt
from aoi_simulator.AoIAgent import AoIAgent
from heapq import heappush
import numpy as np

"""
Extends QueueServer Class from queueing_tool package
- Uses AoIAgent class, wich has agent gen_time

Parameters
    ----------
    **kwargs
        Any :class:`~QueueServer` parameters.
"""

class AoIQueueServer(qt.QueueServer):

    def __init__(self, **kwargs):
        super(AoIQueueServer, self).__init__(**kwargs)
        self.AgentFactory = AoIAgent

    def __repr__(self):
        tmp = ("AoiQueueServer:{0}. Servers: {1}, queued: {2}, arrivals: {3}, "
               "departures: {4}, next time: {5}")
        arg = (self.edge[2], self.num_servers, len(self.queue), self.num_arrivals,
               self.num_departures, round(self._time, 3))
        return tmp.format(*arg)

    # Overrides method to include agent generated time
    def _add_arrival(self, agent=None):
        if agent is not None:
            self._num_total += 1
            heappush(self._arrivals, agent)
        else:
            if self._current_t >= self._next_ct:
                self._next_ct = self.arrival_f(self._current_t)

                if self._next_ct >= self.deactive_t:
                    self._active = False
                    return

                self._num_total += 1
                new_agent = self.AgentFactory((self.edge[2], self._oArrivals), self._next_ct)
                new_agent._time = self._next_ct
                new_agent.gen_time = self._next_ct # agent generated time
                heappush(self._arrivals, new_agent)

                self._oArrivals += 1

                if self._oArrivals >= self.active_cap:
                    self._active = False

        if self._arrivals[0]._time < self._departures[0]._time:
            self._time = self._arrivals[0]._time