import numpy as np
import ast, json

#RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ro = 0.5
mu = 1
# ARRIVAL_TIMES = [1/r for r in RO]
arr_time = 1/(mu*ro)

Q_vector = []
V_vector = []

def calc_aoi(data):
    data = list(data.values())
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
        erro = V_total/((ti_linha-t_inicio)**(2))
        V_vector.append(erro)

    t_fim = ti_linha
    Qi_total = Qi_total + 0.5*(Ti**2)
    m_aoi = Qi_total / (t_fim - t_inicio)
    return m_aoi

def mean_aoi(data_file):    

    with open (data_file, 'r') as d:
        data = json.load(d)
        print("Read")
        #data = ast.literal_eval(data)
    # data_parsed = []
    # for value in data.values():
    #     data_parsed.append(value)
    return calc_aoi(data)

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

print("Processando...")

path = "experimentos/long_sim.txt"
print("Simulated: %f" %mean_aoi(path))

analit_aoi = calc_analitic_aoi(ro, mu)
print("Analytical: %f" %analit_aoi)

arq_nome = "resultados/Q_vec.txt"
with open(arq_nome, 'w') as f:
    f.write(str(Q_vector))

arq_nome = "resultados/V_vec.txt"
with open(arq_nome, 'w') as f:
    f.write(str(V_vector))