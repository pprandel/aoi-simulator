import queueing_tool as qt
from LcfsPreemption import LcfsPreemption
from mean_aoi import mean_aoi
import numpy as np
import json

sim_name = "mm1_2_sources_lcfs_s"
aoi_dic = {}

# Total load in server
RO = list(np.arange(0.4, 0.8, 0.1))
RO = [round(ro,2) for ro in RO]
for ro in RO:
    # individual loads
    print("Simulating for ro: %f" %ro)
    for percent in np.arange(0.1, 0.6, 0.1):
        ro_1 = round(ro*percent, 2)
        ro_2 = round(ro - ro_1, 2)
        print("ro_1: %f ro_2: %f " %(ro_1, ro_2))
        lambda1 = ro_1
        lambda2 = ro_2

        ### Network definition ###
        # Create adjacency matrix
        # Each edge represents a queue and must have a type
        adjacency = {
            0: {2: {'edge_type': 1}},
            1: {2: {'edge_type': 2}},
            2: {3: {'edge_type': 3}}
        }

        G = qt.QueueNetworkDiGraph(adjacency)

        # Define queue classes for each edge type
        q_cl = {1: qt.QueueServer, 2: qt.QueueServer, 3: LcfsPreemption}

        # Queue service rate
        mu = 1
        # Instant service queue
        def f_ser_1(t): return t
        # Exponential service queue
        def f_ser_2(t): return t + np.random.exponential(1/mu)

        # Poisson generation queues (exponential interarrival times)
        def f_gen_1(t): return t+ np.random.exponential(1/lambda1)
        def f_gen_2(t): return t+ np.random.exponential(1/lambda2)

        # Config queues parameters for each edge type
        q_ar = {
            1: {
                'arrival_f': f_gen_1,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            2: {
                'arrival_f': f_gen_2,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            3: {
                'service_f': f_ser_2,
                'num_servers': 1,
                'preemption': 0
            }
        }

        # Instantiate the network
        net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

        # Set queues that collects data
        net.start_collecting_data(queues=2)

        # Initialize queues that generate packets
        net.initialize(queues=range(2))

        # Start simulation with n events
        net.simulate(n=500000)

        # Collect data
        data = net.get_agent_data(queues=2)

        # File where to save simulation data
        arq_nome = "experimentos/" + sim_name + ".json"
        with open(arq_nome, 'w') as f:
            json.dump({str(k):v.tolist() for k, v in data.items()}, f, indent=3)

        # Calculate mean AoI and related RMSE
        aoi = mean_aoi("new_sim", arq_nome, 2)
        key = str(ro) + "_" + str(ro_1) + "_" + str(ro_2)
        aoi_dic[key] = aoi
    arq_nome = "resultados/" + sim_name + ".json"
    with open(arq_nome, 'w') as f:
        json.dump(aoi_dic, f, indent=3)
