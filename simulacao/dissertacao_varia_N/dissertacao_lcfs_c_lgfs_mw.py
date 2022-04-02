import queueing_tool as qt
import numpy as np
import json, os
import aoi_simulator as aoi

# Sim name 
sim_name = "dissertacao_lcfs_c_lgfs_mw"

ro = 5

result = {}

for N in range(30,151,1):
    print("%d fontes:" %N)

    ### Network definition ###
    # Create adjacency matrix
    # Each edge represents a queue and must have a type
    adjacency = {}

    #N = 30
    C = 3
    for i in range(N):
        adjacency[i] = {N: {'edge_type': 1}}
    adjacency[N] = {N+1: {'edge_type': 2}}
    adjacency[N+1] = {N+2: {'edge_type': 3}}
        
            
    G = qt.QueueNetworkDiGraph(adjacency)

    # Define queue classes for each edge type
    q_cl = {1: aoi.LgfsPreemption, 2: aoi.AoIQueueServer, 3: aoi.LgfsMultiServerPreemptionW}

    # Taxa de serviço dos servidores
    mu = 5
    # Taxa de geração das fontes
    lamb = (ro * mu * C) / N

    # Função geração das fontes: determinística
    def f_gen_1(t): return t + 1/lamb

    # Função serviço das fontes
    mu_f = 5 * 0.9**(N/4)
    def f_ser_1(t): 
        return t + (1/mu_f)/0.886 * np.random.weibull(2)

    # Função atraso na rede: 500 ms (média)
    def f_ser_2(t): 
        return t + np.random.exponential(0.5)

    def f_ser_3(t): 
        return t + np.random.exponential(1/mu)

    # Config queues parameters for each edge type
    q_ar = {
        1: {
            'arrival_f': f_gen_1,
            'service_f': f_ser_1,
            'num_servers': 1,
            'preemption': 2,
            'mrl_file': "/home/paulo/Documents/Git/AoI/AoI/data_aux/MRL_weib_2.json"
        },
        2: {
            'service_f': f_ser_2,
            'num_servers': np.infty,
        },
        3: {
            'service_f': f_ser_3,
            'num_servers': C
        }
    }

    # Instantiate the network
    net = aoi.AoIQueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

    # Set queues that collects data
    net.start_collecting_data(queues=N+1)

    # Initialize queues that generate packets
    net.initialize(queues=range(N))

    # Start simulation with n events
    net.simulate(n=200000)

    # Collect data
    data = net.get_AoI_data(monitor=N+1)

    # Criamos uma pasta sim_data para armazenar os dados da simulação, caso ela não exista
    if not os.path.exists('sim_data'):
        os.makedirs('sim_data')

    arq_nome = "sim_data/" + sim_name + "_" + str(N) + "_" + str(ro) + ".json"
    with open(arq_nome, 'w') as f:
        json.dump({str(k):v for k, v in data.items()}, f, indent=3)

    # Calculate mean AoI and related RMSE
    calc_mean = aoi.MeanAoICalc(sim_name, arq_nome, N)
    calc_peak = aoi.MeanPeakAoICalc(sim_name, arq_nome, N)

    print("RO = %f" %(lamb*N/(C*mu)))
    print("Lambda = %f" %(lamb))
    print("mu_f = %f" %(mu_f))

    mean_aoi_vector = []
    mean_peak_vector = []
    preemp_vector = []

    print(calc_mean.aoi)
    for value in calc_mean.aoi.values():
        mean_aoi_vector.append(value["MeanAoI"])
    for value in calc_peak.aoi.values():
        mean_peak_vector.append(value["MeanPeakAoI"])

    print("Mean AoI for all sources:")
    aoi_media = np.mean(mean_aoi_vector)
    print(aoi_media)
    print("Mean Peak AoI for all sources:")
    peak_aoi_media = np.mean(mean_peak_vector)
    print(peak_aoi_media)

    result[str(N)] = {}
    result[str(N)]['MeanAoI'] = aoi_media
    result[str(N)]['MeanPeakAoI'] = peak_aoi_media

arq_nome = "resultados/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump(result, f, indent=3)