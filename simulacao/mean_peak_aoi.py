
"""
Returns the mean peak Age of Information (pAoI)

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
save_pAoI_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of pAoI
    example: "/tmp/my_sim"

Returns
----------
mean_peak_aoi: dict
    dict with sources as keys and mean peak AoI as values
"""

import json
import numpy as np
from scipy.signal import correlate

paoi_vector = []

def calc_RMSE(A_vec, mean_paoi, N):
    # Variance
    var_A = np.var(A_vec)
    # Normalized A
    norm_A = (A_vec - mean_paoi)
    # Autocorrelation
    result = correlate(norm_A, norm_A, mode='same')
    acorr = result [N//2 + 1:]  / (var_A * np.arange(N-1, N//2, -1))
    M = len(acorr)
    iat = 0
    # IAT
    for i in range(M):
        iat = iat + (1 - (i+1)/M)*acorr[i]
    iat = 1 + 2*iat
    print("Integrated autocorrelation times: %f" %iat)
    var_A_mean = var_A/N
    print("Variance of A_mean: %f" %var_A_mean)
    true_var_A_mean = var_A_mean * iat
    print("Variance corrected: %f" %true_var_A_mean)
    RMSE = true_var_A_mean**0.5
    print("RMSE: %f" %RMSE)
    return RMSE
    

def calc_peak_aoi(data):
    paoi_vector.clear()
    
    # peak age calculation
    def Ai(Ti, Yi):
        return Ti + Yi
    
    ti = data[0][0][0] # Chegada t0
    t_inicio = ti
    Ai_total = 0
    N = 0 # total delivered packets
    data.pop(0) # Remove first entry
    for value in data:
        if value[0][2] == 0: 
            continue
        N = N + 1 # delivered packet
        Yi = value[0][0] - ti
        ti = value[0][0]
        ti_linha = value[0][2]
        Ti = ti_linha - ti
        paoi_vector.append(Ai(Ti, Yi))
    mean_paoi = np.mean(paoi_vector)
    print("Mean pAoI: %f" %mean_paoi)
    RMSE = calc_RMSE(paoi_vector, mean_paoi, N)
    print("Last packet index: #%d" %N)
    return (mean_paoi, RMSE)

def mean_peak_aoi(sim_id, data_file, num_sources, save_pAoI_seq="None"):
    print("Calculating mean pAoI values for simulation #%s" %sim_id)
    # Initialize return dict
    paoi = {}
    for i in range(num_sources):
        paoi[i] = {}
        paoi[i]["MeanPAoI"] = np.inf
        paoi[i]["RMSE"] = 0
    # Load data
    with open (data_file, 'r') as d:
        data = json.load(d)
    # Split sources
    splitted_data = {}
    for id, value in data.items():
        source = int(id.split(",")[0][1:])
        if source in splitted_data:
            splitted_data[source].append(value)
        else:
            splitted_data[source] = []
            splitted_data[source].append(value)

    # Calculate AoI per source
    for i in splitted_data.keys():
        print("Source %d:" %i)
        try:
            result = calc_peak_aoi(splitted_data[i])
        except Exception as e:
            print("Error calculating pAoI for source %d" %i)
        paoi[i]["MeanPAoI"] = result[0]
        paoi[i]["RMSE"] = result[1]

        if save_pAoI_seq != "None":
            try:
                arq_name = save_pAoI_seq + "/" + sim_id + "_source_" + str(i) + ".txt"
                with open(arq_name, 'w') as f:
                    f.write(str(paoi_vector))
            except Exception as e:
                print("Error saving pAoI sequence: %s" %e)
    return paoi