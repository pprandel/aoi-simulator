import queueing_tool as qt
import numpy as np

"""
Last Come First Served Queue with finite capacity and preemption (optional)

Parameters
    ----------
    preemption : int (0 (default): no preemption, 1: preemption in service, 2: preemption in waiting)
        Preemption in service: last arrival 
    **kwargs
        Any :class:`~QueueServer` or `LossQueue` parameters.
"""

class LcfsPreemption(qt.LossQueue):

    def __init__(self, preemption=0, **kwargs):
        super(LcfsPreemption, self).__init__(**kwargs)
        self.preemption = preemption

    def next_event(self):

        if self._departures[0]._time < self._arrivals[0]._time:
            return super(LossQueue, self).next_event()
        elif self._arrivals[0]._time < infty:
            if self.num_system < self.num_servers + self.buffer:
                super(LossQueue, self).next_event()
            else:
                self.num_blocked += 1
                self._num_total -= 1

                arrival = heappop(self._arrivals)
                arrival.add_loss(self.edge)

                self._current_t = arrival._time

                if self._active:
                    self._add_arrival()

                if self.collect_data:
                    if arrival.agent_id in self.data:
                        self.data[arrival.agent_id].append([arrival._time, 0, 0, len(self.queue), self.num_system])
                    else:
                        self.data[arrival.agent_id] = [[arrival._time, 0, 0, len(self.queue), self.num_system]]

                if self._arrivals[0]._time < self._departures[0]._time:
                    self._time = self._arrivals[0]._time
                else:
                    self._time = self._departures[0]._time

RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/r for r in RO]

mean_delay = {}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = qt.QueueServer(1, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=10000, nD=10000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))
