import queueing_tool as qt
import numpy as np
import json, os
import aoi_simulator as aoi

# Sim name 
sim_name = "maf_lgfs_mw_preemption_exp"

aoi_dic = {}
RO = np.arange(0.2, 3.1, 0.2)
#RO = np.arange(0.1, 1.1, 0.1)
RO = np.around(RO, decimals=1)
for ro in RO:

    ### Network definition ###
    # Create adjacency matrix
    # Each edge represents a queue and must have a type
    adjacency = {}
    N = 50
    C = 3
    for i in range(N):
        adjacency[i] = {N: {'edge_type': 1}}
    adjacency[N] = {N+1: {'edge_type': 2}}
    adjacency[N+1] = {N+2: {'edge_type': 3}}
        
            
    G = qt.QueueNetworkDiGraph(adjacency)

    # Define queue classes for each edge type
    q_cl = {1: aoi.AoIQueueServer, 2: aoi.AoIQueueServer, 3: aoi.LgfsMultiServerPreemptionW}

    # Taxa de serviço dos servidores
    mu = 5
    # Taxa de geração das fontes
    lamb = (ro * mu * C) / N

    # Função geração das fontes
    def f_gen_1(t): return t + np.random.exponential(1/lamb)

    def f_ser_1(t): return t

    # Função atraso na rede: 500 ms (média)
    def f_ser_2(t): return t + np.random.exponential(0.5)


    def f_ser_3(t): return t + np.random.exponential(1/mu)

    # Config queues parameters for each edge type
    q_ar = {
        1: {
            'arrival_f': f_gen_1,
            'service_f': f_ser_1,
            'num_servers': 1
        },
        2: {
            'service_f': f_ser_2,
            'num_servers': np.infty,
        },
        3: {
            'service_f': f_ser_3,
            'num_servers': C,
            #'policy': 1
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

    arq_nome = "sim_data/" + sim_name + ".json"
    with open(arq_nome, 'w') as f:
        json.dump({str(k):v for k, v in data.items()}, f, indent=3)

    print("RO = %f" %(ro))
    print("Lambda = %f" %(lamb))
    # Calculate mean AoI and related RMSE
    calc = aoi.MeanAoICalc(sim_name, arq_nome, N)
    print(calc.aoi)
    aoi_vector = []
    for value in calc.aoi.values():
        aoi_vector.append(value["MeanAoI"])
    print("Mean AoI for all sources:")
    media = np.mean(aoi_vector)
    print(media)
    aoi_dic[ro] = media

arq_nome = "resultados/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump(aoi_dic, f, indent=3)