
"""
Returns the mean Age of Information (AoI)

Parameters
----------
sim_id: str
    identification of simulation
data_file : json file
    json with class:Agent "agent_id" as keys and list [arrival, service
    start, departure times, agents waiting to be served and the total agents in the
    system] as values
num_sources: int
    number of sources of Agents. Mean AoI will be calculated for each source - Integer
save_AoI_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI
    example: "/tmp/my_sim"
save_Q_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI areas Q
    example: "/tmp/my_sim"

Returns
----------
mean_aoi: dict
    dict with sources as keys and mean AoI as values
"""

import json
import numpy as np
from numpy.core.fromnumeric import var 
from scipy.signal import correlate

aoi_vector = []
Q_vector = []

def calculate_RMSE(Q, N, tau):
    # Q mean and variance
    n = len(Q)
    mean_q = np.mean(Q)
    var_q = np.var(Q)
    # Normalized Q
    norm_Q = (Q - mean_q)
    # Autocorrelation
    result = correlate(norm_Q, norm_Q, mode='same')
    acorr = result [n//2 + 1:]  / (np.var(Q) * np.arange(n-1, n//2, -1))
    M = len(acorr)
    iat = 0
    # IAT
    for i in range(M):
            iat = iat + (1 - (i+1)/M)*acorr[i]
    iat = 1 + 2*iat
    print("Integrated autocorrelation times: %f" %iat)
    var_Q_mean = var_q/len(Q)
    print("Variance of Q_mean: %f" %var_Q_mean)
    true_var_Q_mean = var_Q_mean * iat
    print("Variance corrected: %f" %true_var_Q_mean)
    var_aoi_mean = (N/tau)**2 * true_var_Q_mean
    RMSE = var_aoi_mean**0.5
    print("RMSE: %f" %RMSE)
    return RMSE
    

def calc_aoi(data):
    aoi_vector.clear()
    Q_vector.clear()
    
    def Qi(Ti, Yi):
        Q = Ti*Yi + 0.5*(Yi**2)
        return Q
    
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
        Qi_now = Qi(Ti, Yi)
        Qi_total = Qi_total + Qi_now
        mean_aoi = Qi_total/(ti_linha-t_inicio)
        aoi_vector.append(mean_aoi)
        Q_vector.append(Qi_now)
        last_packet = (i, ti_linha)
    t_fim = ti_linha
    Qi_total = Qi_total + 0.5*(Ti**2)
    m_aoi = Qi_total / (t_fim - t_inicio)
    print("Mean AoI: %f" %mean_aoi)
    N = last_packet[0]
    tau = last_packet[1]
    RMSE = calculate_RMSE(Q_vector, N, tau)
    print("Last packet index: #%d" %N)
    return (m_aoi, RMSE)

def mean_aoi(sim_id, data_file, num_sources, save_AoI_seq="None", save_Q_seq="None"):
    print("Calculating mean AoI values for simulation #%s" %sim_id)
    # Initialize return dict
    aoi = {}
    for i in range(num_sources):
        aoi[i] = {}
        aoi[i]["MeanAoI"] = np.inf
        aoi[i]["RMSE"] = 0
    # Load data
    with open (data_file, 'r') as d:
        data = json.load(d)
    # Split sources
    splitted_data = {}
    for id, value in data.items():
        source = int(id[1])
        if source in splitted_data:
            splitted_data[source].append(value)
        else:
            splitted_data[source] = []
            splitted_data[source].append(value)

    # Calculate AoI per source
    for i in splitted_data.keys():
        print("Source %d:" %i)
        try:
            result = calc_aoi(splitted_data[i])
        except Exception as e:
            print("Error calculating AoI for source %d" %i)
        aoi[i]["MeanAoI"] = result[0]
        aoi[i]["RMSE"] = result[1]

        if save_AoI_seq != "None":
            try:
                arq_name = save_AoI_seq + "/" + sim_id + "_source_" + str(i) + ".txt"
                with open(arq_name, 'w') as f:
                    f.write(str(Q_vector))
            except Exception as e:
                print("Error saving AoI sequence: %s" %e)

        if save_Q_seq != "None":
            try:
                arq_name = save_Q_seq + "/" + sim_id + "_source_" + str(i) + ".txt"
                with open(arq_name, 'w') as f:
                    f.write(str(Q_vector))
            except Exception as e:
                print("Error saving Q sequence: %s" %e)

    return aoi