from LcfsPreemption import LcfsPreemption
import numpy as np

RO = list(np.arange(0.1, 2, 0.1))
ARRIVAL_TIMES = [1/r for r in RO]

mean_delay = {}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = LcfsPreemption(preemption=1, num_servers=1, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=10000, nD=10000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/mm1_lcfs_w/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))
