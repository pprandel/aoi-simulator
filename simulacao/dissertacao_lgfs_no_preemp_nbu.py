import queueing_tool as qt
import numpy as np
import json, os
import aoi_simulator as aoi

# Sim name 
sim_name = "lgfs_no_preemption_nbu"

### Network definition ###
# Create adjacency matrix
# Each edge represents a queue and must have a type
adjacency = {}
ro = 0.95
N = 50
C = 3
for i in range(N):
    adjacency[i] = {N: {'edge_type': 1}}
adjacency[N] = {N+1: {'edge_type': 2}}
adjacency[N+1] = {N+2: {'edge_type': 3}}
      
        
G = qt.QueueNetworkDiGraph(adjacency)

# Define queue classes for each edge type
q_cl = {1: aoi.AoIQueueServer, 2: aoi.AoIQueueServer, 3: aoi.LgfsMultiServerNoPreemption}

# Taxa de serviço dos servidores
mu = 5
# Taxa de geração das fontes
lamb = (ro * mu * C) / N

# Função geração das fontes: determinística
def f_gen_1(t): return t + 1/lamb

# Função serviço das fontes
mu_f = 10 - 0.1*N
def f_ser_1(t): 
   return t + np.random.exponential(1/mu_f)

# Função atraso na rede: 500 ms (média)
def f_ser_2(t): 
   return t + np.random.exponential(0.5)


def f_ser_3(t): return t + (1/mu)/0.886 * np.random.weibull(2)

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
        'policy': 2
    }
}

# Instantiate the network
net = aoi.AoIQueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

# Set queues that collects data
net.start_collecting_data(queues=N+1)

# Initialize queues that generate packets
net.initialize(queues=range(N))

# Start simulation with n events
net.simulate(n=100000)

# Collect data
data = net.get_AoI_data(monitor=N+1)

# Criamos uma pasta sim_data para armazenar os dados da simulação, caso ela não exista
if not os.path.exists('sim_data'):
    os.makedirs('sim_data')

arq_nome = "sim_data/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump({str(k):v for k, v in data.items()}, f, indent=3)

# Calculate mean AoI and related RMSE
calc = aoi.MeanAoICalc(sim_name, arq_nome, N)
print(calc.aoi)

print("RO = %f" %(lamb*N/(C*mu)))
print("Lambda = %f" %(lamb))
print("mu_f = %f" %(mu_f))

aoi_vector = []
for value in calc.aoi.values():
    aoi_vector.append(value["MeanAoI"])
print("Mean AoI for all sources:")
print(np.mean(aoi_vector))
