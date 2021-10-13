import queueing_tool as qt
from LgfsMultiServerPreemption import LgfsMultiServerPreemption
from AoIQueueServer import AoiQueueServer
from mean_aoi import mean_aoi
import numpy as np
import json
import scipy.stats as st

# Sim name 
sim_name = "mm1_N_sources_lgfs_preemption"

### Network definition ###
# Create adjacency matrix
# Each edge represents a queue and must have a type
adjacency = {}
N = 30
for i in range(N):
    adjacency[i] = {N: {'edge_type': 1}}
adjacency[N] = {N+1: {'edge_type': 2}}
adjacency[N+1] = {N+2: {'edge_type': 3}}
        
        
G = qt.QueueNetworkDiGraph(adjacency)

# Define queue classes for each edge type
q_cl = {1: AoiQueueServer, 2: AoiQueueServer, 3: LgfsMultiServerPreemption}

# Define packet generation and service functions
# Packet generation rates
lamb = 1
# Queue service rate
mu = 10
# Poisson generation queues (exponential interarrival times)
def f_gen_1(t): return t+ np.random.exponential(1/lamb)
# Instant service queue
def f_ser_1(t): return t
# Exponential service queue
def f_ser_2(t): return t + np.random.exponential(0.5)
# Exponential service queue
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
        'num_servers': 5,
    },
    3: {
        'service_f': f_ser_3,
        'num_servers': 3,
        'policy': 2
    }
}

# Instantiate the network
net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

# Set queues that collects data
net.start_collecting_data(queues=N+1)

# Initialize queues that generate packets
net.initialize(queues=range(N))

# Start simulation with n events
net.simulate(n=100000)

# Collect data
data = net.get_agent_data(queues=N+1)

# File where to save simulation data
arq_nome = "experimentos/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump({str(k):v.tolist() for k, v in data.items()}, f, indent=3)

# Calculate mean AoI and related RMSE
result = mean_aoi(sim_name, arq_nome, N)
print(result)
aoi_vector = []
for source in result.values():
    aoi_vector.append(source["MeanAoI"])
print("Mean AoI for all sources:")
print(np.mean(aoi_vector))
