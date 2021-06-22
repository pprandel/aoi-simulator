
"""
Returns the mean Age of Information (AoI)

Parameters
----------
data_file : path to txt file - python dict like
    Dict with class:Agent "agent_id" keys and values as a list with: arrival, service
        start, departure times, agents waiting to be served and the total agents in the
        system

Returns
----------
mean_aoi: float with the mean AoI of the Agent's information at departure node in relation
with the information at the source node
"""

import ast

def mean_aoi(data_file):
    
    def Qi(Ti, Yi):
        return 0.5*(Ti + Yi)**2 - 0.5*Ti**2

    with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

    ti = data[(0,0)][0][0] # Chegada t0
    t_inicio = ti
    Qi_total = 0
    data.pop((0,0)) # Remove a primeira entrada

    for value in data.values():
        if value[0][2] == 0: 
            t_fim = ti
            m_aoi = Qi_total / (t_fim - t_inicio)
            return m_aoi
        Yi = value[0][0] - ti
        ti = value[0][0]
        Ti = value[0][2] - ti
        Qi_total = Qi_total + Qi(Ti, Yi)
    t_fim = ti
    m_aoi = Qi_total / (t_fim - t_inicio)
    return m_aoi