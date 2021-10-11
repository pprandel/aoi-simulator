from queueing_tool.queues.agents import Agent

"""
Extends Agent Class from queueing_tool package
- Includes generated time in agent attributes

Parameters
    ----------
    **kwargs
        Any :class:`~Agent` parameters.
"""

class AoiAgent(Agent):

    def __init__(self, agent_id, **kwargs):
        super(AoiAgent, self).__init__(agent_id, **kwargs)
        self.gen_time = 0

    def __repr__(self):
        return "AoIAgent; agent_id:{0}. time: {1}. gen_time: {2}".format(self.agent_id, round(self._time, 3), round(self.gen_time,3))
