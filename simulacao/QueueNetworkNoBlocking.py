import queueing_tool as qt
import numpy as np

"""
Extends QueueNetwork Class from queueing_tool package
Prevent blocking of agents moving between queues

Parameters
    ----------
    **kwargs
        Any :class:`~QueueNetwork` parameters.
"""

class QueueNetworkNoBlocking(qt.QueueNetwork):

    def __init__(self, **kwargs):
        super(QueueNetworkNoBlocking, self).__init__(**kwargs)

    def _simulate_next_event(self, slow=True):
        if self._fancy_heap.size == 0:
            self._t = np.infty
            return

        q1k = self._fancy_heap.pop()
        q1t = q1k[0]
        q1 = self.edge2queue[q1k[1]]
        e1 = q1.edge[2]

        event = q1.next_event_description()
        self._t = q1t
        self._qkey = q1k
        self.num_events += 1

        if event == 2:  # This is a departure
            e2 = q1._departures[0].desired_destination(self, q1.edge)
            q2 = self.edge2queue[e2]
            q2k = q2._key()

            agent = q1.next_event()
            agent._time = q1t

            q2._add_arrival(agent)
            self.num_agents[e1] = q1._num_total
            self.num_agents[e2] = q2._num_total

            if slow:
                self._update_graph_colors(qedge=q1.edge)
                self._prev_edge = q1.edge

            if q2._active and self.max_agents < np.infty and \
                    np.sum(self.num_agents) > self.max_agents - 1:
                q2._active = False

            q2.next_event()
            self.num_agents[e2] = q2._num_total

            if slow:
                self._update_graph_colors(qedge=q2.edge)
                self._prev_edge = q2.edge

            new_q1k = q1._key()
            new_q2k = q2._key()

            if new_q2k[0] != q2k[0]:
                self._fancy_heap.push(*new_q2k)

                if new_q1k[0] < np.infty and new_q1k != new_q2k:
                    self._fancy_heap.push(*new_q1k)
            else:
                if new_q1k[0] < np.infty:
                    self._fancy_heap.push(*new_q1k)

        elif event == 1:  # This is an arrival
            if q1._active and self.max_agents < np.infty and \
                    np.sum(self.num_agents) > self.max_agents - 1:
                q1._active = False

            q1.next_event()
            self.num_agents[e1] = q1._num_total

            if slow:
                self._update_graph_colors(qedge=q1.edge)
                self._prev_edge = q1.edge

            new_q1k = q1._key()
            if new_q1k[0] < np.infty:
                self._fancy_heap.push(*new_q1k)