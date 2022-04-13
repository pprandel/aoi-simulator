from LcfsMultiServer import LcfsMultiServer
import numpy as np
import json

C = 4
RO = list(np.arange(0.1, 2, 0.1))
ARRIVAL_TIMES = [1/(r*C) for r in RO]

mean_delay = {}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = LcfsMultiServer(num_servers=C, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=15000, nD=15000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/2_servers_lcfs_mm1/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
       json.dump({str(k):v for k, v in data.items()}, f)
