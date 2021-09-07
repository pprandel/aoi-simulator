
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
import numpy as np 

# def calc_aoi(data):

#     def Qi(Ti, Yi):
#         Q = Ti*Yi + 0.5*(Yi**2)
#         return Q
    
#     ti = data[0][0][0] # Chegada t0
#     t_inicio = ti
#     Qi_total = 0
#     data.pop(0) # Remove a primeira entrada
#     for i, value in enumerate(data):
#         if value[0][2] == 0: 
#             print("Terminated on agent #%d" %(i))
#             t_fim = ti_linha
#             Qi_total = Qi_total + 0.5*(Ti**2)
#             m_aoi = Qi_total / (t_fim - t_inicio)
#             return m_aoi
#         Yi = value[0][0] - ti
#         ti = value[0][0]
#         ti_linha = value[0][2]
#         Ti = ti_linha - ti
#         Qi_total = Qi_total + Qi(Ti, Yi)
#     t_fim = ti_linha
#     Qi_total = Qi_total + 0.5*(Ti**2)
#     m_aoi = Qi_total / (t_fim - t_inicio)
#     return m_aoi

Q_vector = []
V_vector = []

def calc_aoi(data):
    Q_vector.clear()
    V_vector.clear()
    def Qi(Ti, Yi):
        Q = Ti*Yi + 0.5*(Yi**2)
        return Q
    
    ti = data[0][0][0] # Chegada t0
    t_inicio = ti
    Qi_total = 0
    V_total = 0
    data.pop(0) # Remove a primeira entrada
    for i, value in enumerate(data):
        if value[0][2] == 0: 
            print("Terminated on agent #%d" %(i))
            t_fim = ti_linha
            Qi_total = Qi_total + 0.5*(Ti**2)
            Q_vector.append(Qi_total/(ti_linha-t_inicio))
            m_aoi = Qi_total / (ti_linha-t_inicio)
            return m_aoi
        Yi = value[0][0] - ti
        ti = value[0][0]
        ti_linha = value[0][2]
        Ti = ti_linha - ti
        Qi_atual = Qi(Ti, Yi)
        Qi_total = Qi_total + Qi_atual
        age_media = Qi_total/(ti_linha-t_inicio)
        Q_vector.append(age_media)
        V_total = V_total + (Qi_atual - Qi_total/(i+1))**2
        erro = V_total/((ti_linha-t_inicio)**2)
        V_vector.append(erro)

    t_fim = ti_linha
    Qi_total = Qi_total + 0.5*(Ti**2)
    m_aoi = Qi_total / (t_fim - t_inicio)
    return m_aoi

def calc_aoi_lcfs(data):
    
    def Qi(Ti, Yi):
        return Ti*Yi + 0.5*(Yi**2)

    ti = data[0][0][0] # Chegada t0
    t_inicio = ti
    Qi_total = 0
    data.pop(0) # Remove a primeira entrada

    for i, value in enumerate(data):
        if value[0][2] == 0: 
            continue
        Yi = value[0][0] - ti
        ti = value[0][0]
        ti_linha = value[0][2]
        Ti = ti_linha - ti
        Qi_total = Qi_total + Qi(Ti, Yi)
    t_fim = ti_linha
    Qi_total = Qi_total + 0.5*(Ti**2)
    m_aoi = Qi_total / (t_fim - t_inicio)
    print("Terminated on agent #%d" %(i))
    return m_aoi

def mean_aoi(data_file):    

    with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

    data_parsed = []
    for value in data.values():
        data_parsed.append(value)
    return calc_aoi(data_parsed)
    
def mean_aoi_lcfs(data_file):    

    with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

    data_parsed = []
    for value in data.values():
        data_parsed.append(value)
    return calc_aoi_lcfs(data_parsed)

def mean_aoi_n_fontes(data_file, n):
    
    aoi = {}
    for i in range(n):
        aoi[i] = np.inf

    with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)
    
    data_por_fonte = {}

    # Separa as fontes
    for id, value in data.items():
        fonte = id[0]
        if fonte in data_por_fonte:
            data_por_fonte[fonte].append(value)
        else:
            data_por_fonte[fonte] = []

    # Calcula AoI por fonte
    for i in data_por_fonte.keys():
        aoi[i] = calc_aoi(data_por_fonte[i])

        arq_nome = "resultados/Q_vec_" + str(i) + ".txt"
        with open(arq_nome, 'w') as f:
            f.write(str(Q_vector))

        arq_nome = "resultados/V_vec_" + str(i) + ".txt"
        with open(arq_nome, 'w') as f:
            f.write(str(V_vector))

    return aoi

def mean_aoi_n_fontes_lcfs(data_file, n):
    
    aoi = {}
    for i in range(n):
        aoi[i] = np.inf

    with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)
    
    data_por_fonte = {}

    # Separa as fontes
    for id, value in data.items():
        fonte = id[0]
        if fonte in data_por_fonte:
            data_por_fonte[fonte].append(value)
        else:
            data_por_fonte[fonte] = []

    # Calcula AoI por fonte
    for i in data_por_fonte.keys():
        aoi[i] = calc_aoi_lcfs(data_por_fonte[i])

    return aoi