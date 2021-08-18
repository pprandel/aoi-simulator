import queueing_tool as qt
from LcfsPreemption import LcfsPreemption
import numpy as np
import sys

# RO total no servidor
RO = list(np.arange(0.2, 3, 0.4))
RO = [round(ro,2) for ro in RO]
for ro in RO:
    # ro das fontes
    print("Simulando para ro: %f" %ro)
    for percent in np.arange(0, 1.1, 0.1):
        ro_1 = round(ro*percent, 2)
        ro_2 = round(ro - ro_1, 2)
        print("ro_1: %f ro_2: %f " %(ro_1, ro_2))
        if ro_1 ==0:
            arr_1 = 0
        else:
            arr_1 = 1/ro_1
        if ro_2 ==0:
            arr_2 = 0
        else:
            arr_2 = 1/ro_2

        adjacency = {
            0: {2: {'edge_type': 1}},
            1: {2: {'edge_type': 2}},
            2: {3: {'edge_type': 3}}
        }
        
        G = qt.QueueNetworkDiGraph(adjacency)
        q_cl = {1: qt.QueueServer, 2: qt.QueueServer, 3: LcfsPreemption}
        def f_arr_1(t): return t+ np.random.exponential(arr_1)
        def f_arr_2(t): return t+ np.random.exponential(arr_2)
        def f_ser_1(t): return t
        def f_ser_2(t): return t + np.random.exponential(1)
        q_ar = {
            1: {
                'arrival_f': f_arr_1,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            2: {
                'arrival_f': f_arr_2,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            3: {
                'service_f': f_ser_2,
                'num_servers': 1,
                'preemption': 0
            }
        }
        net = qt.QueueNetwork(g=G, q_classes=q_cl, q_args=q_ar)
        net.start_collecting_data()
        if arr_1 == 0:
            net.initialize(queues=[1])
        elif arr_2 == 0:
            net.initialize(queues=[0])
        else:
            net.initialize(queues=[0,1])
        net.simulate(n=50000)
        fila_2 = net.edge2queue[2]
        data = fila_2.data
        arq_nome = "experimentos/duas_fontes/mm1_lcfs_s/ro_" + str(ro) + "_" + str(ro_1) + "_" + str(ro_2) + ".txt"
        with open(arq_nome, 'w') as f:
            f.write(str(data))

