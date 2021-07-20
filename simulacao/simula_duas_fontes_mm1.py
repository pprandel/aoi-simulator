import queueing_tool as qt
import numpy as np
import sys

RO = list(np.arange(0.1, 1, 0.1))
ARRIVAL_TIMES = [2/r for r in RO]

adjacency = {
    0: {2: {'edge_type': 1}},
    1: {2: {'edge_type': 1}},
    2: {3: {'edge_type': 2}}
}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    G = qt.QueueNetworkDiGraph(adjacency)
    q_cl = {1: qt.QueueServer, 2: qt.QueueServer}
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser_1(t): return t
    def ser_2(t): return t + np.random.exponential(1)
    q_ar = {
        1: {
            'arrival_f': arr,
            'service_f': ser_1,
            'num_servers': 1
        },
        2: {
            'service_f': ser_2,
            'num_servers': 1
        }
    }
    net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar)
    net.start_collecting_data()
    net.initialize(queues=[0,1])
    net.simulate(n=20000)
    fila_2 = net.edge2queue[2]
    data = fila_2.data
    arq_nome = "experimentos/duas_fontes/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))

