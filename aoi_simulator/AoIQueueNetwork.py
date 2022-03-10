import queueing_tool as qt
import numpy as np
import collections
import numbers

"""
Extends QueueNetwork Class from queueing_tool package
- Includes a method to fetch data for AoI calculation

Parameters
    ----------
    **kwargs
        Any :class:`~QueueNetwork` parameters.
"""

class AoiQueueNetwork(qt.QueueNetwork):


    def __init__(self, **kwargs):
        super(AoiQueueNetwork, self).__init__(**kwargs)

    def __repr__(self):
        the_string = 'AoiQueueNetwork. # nodes: {0}, edges: {1}, agents: {2}'
        return the_string.format(self.nV, self.nE, np.sum(self.num_agents))

    def get_AoI_data(self, monitor=None):
        """Gets data from queues related to AoI.

        Parameters
        ----------
        monitor : int
            The edge index identifying the monitor where updates are delivered.

        Returns
        -------
        dict
            Returns a ``dict`` where the keys are the
            :class:`Agent's<.Agent>` ``agent_id`` and the values are
            :class:`ndarrays<~numpy.ndarray>` for that
            :class:`Agent's<.Agent>` data. The columns of this array
            are as follows:

            * First: The generation time of an agent (update) at his source.
            * Second: The start of service time of an agent (update) at the monitor.
            * Third: The departure time of an agent (update) at the monitor.
        """

        queues = _get_queues(self.g, monitor, None, None)
        monitor_queue = queues[0]
        data = {}
        for agent_id, dat in self.edge2queue[monitor_queue].data.items():
            datum = dat[0][0:3]
            if agent_id in data:
                data[agent_id] = np.vstack((data[agent_id], datum))
            else:
                data[agent_id] = datum
        return data

def _get_queues(g, queues, edge, edge_type):
    """Used to specify edge indices from different types of arguments."""
    INT = numbers.Integral
    if isinstance(queues, INT):
        queues = [queues]

    elif queues is None:
        if edge is not None:
            if isinstance(edge, tuple):
                if isinstance(edge[0], INT) and isinstance(edge[1], INT):
                    queues = [g.edge_index[edge]]
            elif isinstance(edge[0], collections.Iterable):
                if np.array([len(e) == 2 for e in edge]).all():
                    queues = [g.edge_index[e] for e in edge]
            else:
                queues = [g.edge_index[edge]]
        elif edge_type is not None:
            if isinstance(edge_type, collections.Iterable):
                edge_type = set(edge_type)
            else:
                edge_type = set([edge_type])
            tmp = []
            for e in g.edges():
                if g.ep(e, 'edge_type') in edge_type:
                    tmp.append(g.edge_index[e])

            queues = np.array(tmp, int)

        if queues is None:
            queues = range(g.number_of_edges())

    return queues