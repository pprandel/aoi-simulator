import queueing_tool as qt
from LcfsMultiServer import LcfsMultiServer
from mean_peak_aoi import  mean_peak_aoi
import numpy as np
import json

sim_name = "mm1_basic_peak"
aoi_dic = {}
RO = np.arange(0.1, 1, 0.1)
RO = np.around(RO, decimals=1)
for ro in RO:

    ### Network definition ###
    # Create adjacency matrix
    # Each edge represents a queue and must have a type
    adjacency = {}
    N = 1
    for i in range(N):
        adjacency[i] = {N: {'edge_type': 1}}
    adjacency[N] = {N+1: {'edge_type': 2}}
            
            
    G = qt.QueueNetworkDiGraph(adjacency)

    # Define queue classes for each edge type
    q_cl = {1: qt.QueueServer, 2: qt.QueueServer}

    # Define packet generation and service functions
    # Queue service rate
    mu = 1
    # Packet generation rates
    lamb = mu * ro
    # Poisson generation queues (exponential interarrival times)
    def f_gen_1(t): return t+ np.random.exponential(1/lamb)
    # Instant service queue
    def f_ser_1(t): return t
    # Exponential service queue
    def f_ser_2(t): return t + np.random.exponential(1/mu)

    # Config queues parameters for each edge type
    q_ar = {
        1: {
            'arrival_f': f_gen_1,
            'service_f': f_ser_1,
            'num_servers': 1
        },
        2: {
            'service_f': f_ser_2,
            'num_servers': 1
        }
    }

    # Instantiate the network
    net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

    # Set queues that collects data
    net.start_collecting_data(queues=N)

    # Initialize queues that generate packets
    net.initialize(queues=range(N))

    # Start simulation with n events
    net.simulate(n=500000)

    # Collect data
    data = net.get_agent_data(queues=N)

    # File where to save simulation data
    arq_nome = "experimentos/" + sim_name + "_ro_" + str(ro) + ".json"
    with open(arq_nome, 'w') as f:
        json.dump({str(k):v for k, v in data.items()}, f, indent=3)

    # Calculate mean AoI and related RMSE
    aoi = mean_peak_aoi(sim_name, arq_nome, N)
    print(aoi)
    aoi_dic[str(ro)] = aoi[0]
arq_nome = "resultados/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump(aoi_dic, f, indent=3)