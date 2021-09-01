import queueing_tool as qt
import numpy as np

C = 1
RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/(r*C) for r in RO]

mean_delay = {}

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = qt.QueueServer(num_servers=C, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=50000, nD=50000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/2_servers_mm1/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))
