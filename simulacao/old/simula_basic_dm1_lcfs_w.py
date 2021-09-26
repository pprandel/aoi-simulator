from LcfsPreemption import LcfsPreemption
import numpy as np
import os

RO = list(np.arange(0.1, 2, 0.1))
ARRIVAL_TIMES = [1/r for r in RO]

mean_delay = {}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t + arr_time
    def ser(t): return t + np.random.exponential(1)
    q = LcfsPreemption(preemption=1, num_servers=1, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=10000, nD=10000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/dm1_lcfs_w/mm1_ro_" + str(RO[i]) + ".txt"
    if not os.path.exists('experimentos/dm1_lcfs_w'):
        os.makedirs('experimentos/dm1_lcfs_w')
    with open(arq_nome, 'w') as f:
        f.write(str(data))
