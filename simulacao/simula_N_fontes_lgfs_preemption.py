from numpy.lib.function_base import sinc
import queueing_tool as qt
from LgfsMultiServerPreemption import LgfsMultiServerPreemption
from AoIQueueServer import AoiQueueServer
from mean_aoi import mean_aoi
import numpy as np
import json

# Sim name 
sim_name = {0: "N_sources_lgfs_preemption", 1: "N_sources_lgfs_preemption_MAX", 2: "N_sources_lgfs_preemption_MASIF"}

# Num sources
N = 30
# Num servers
num_servers = 3

for preemption, sim in sim_name.items():
    print("Starting %s" %sim)
    aoi_dic = {}
    # Total load in server
    RO = list(np.arange(0.2, 2.3, 0.2))
    RO = [round(ro,2) for ro in RO]
    for ro in RO:
        print("RO = %f" %ro)
        ### Network definition ###
        # Create adjacency matrix
        # Each edge represents a queue and must have a type
        adjacency = {}
        for i in range(N):
            adjacency[i] = {N: {'edge_type': 1}}
        adjacency[N] = {N+1: {'edge_type': 2}}                
                
        G = qt.QueueNetworkDiGraph(adjacency)

        # Define queue classes for each edge type
        q_cl = {1: AoiQueueServer, 2: LgfsMultiServerPreemption}

        # Queue service rate
        mu = 1
        # Packet generation rates
        lamb = ro * mu * num_servers / N
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
                'num_servers': num_servers,
                'preemption': preemption
            }
        }

        # Instantiate the network
        net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

        # Set queues that collects data
        net.start_collecting_data(queues=N)

        # Initialize queues that generate packets
        net.initialize(queues=range(N))

        # Start simulation with n events
        net.simulate(n=1000000)

        # Collect data
        data = net.get_agent_data(queues=N)

        # File where to save simulation data
        arq_nome = "experimentos/" + sim + ".json"
        with open(arq_nome, 'w') as f:
            json.dump({str(k):v.tolist() for k, v in data.items()}, f, indent=3)

        # Calculate mean AoI and related RMSE
        aoi = mean_aoi(sim, arq_nome, N)
        print(aoi)
        age_vector = []
        rmse_vector = []
        for source in aoi.values():
            age_vector.append(source["MeanAoI"])
            rmse_vector.append(source["RMSE"])
        aoi_dic[str(ro)] = {"MeanAoI": np.mean(age_vector), "MaxRMSE": np.max(rmse_vector)}
    arq_nome = "resultados/" + sim + ".json"
    with open(arq_nome, 'w') as f:
        json.dump(aoi_dic, f, indent=3)