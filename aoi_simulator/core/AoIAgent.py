from queueing_tool.queues.agents import Agent

"""
Extends Agent Class from queueing_tool package
- Includes generated time in agent attributes

Parameters
    ----------
    **kwargs
        Any :class:`~Agent` parameters.
"""

class AoIAgent(Agent):

    def __init__(self, agent_id=(0, 0), gen_time=0, **kwargs):
        new_agent_id = (agent_id[0], agent_id[1], gen_time)
        super(AoIAgent, self).__init__(new_agent_id, **kwargs)
        self.gen_time = 0
   
    def __repr__(self):
        return "AoIAgent; agent_id:{0}. time: {1}. gen_time: {2}".format(self.agent_id, round(self._time, 3), round(self.gen_time,3))
