import queueing_tool as qt
import numpy as np
from LcfsMultiServerReassign import LcfsMultiServerReassign

# Nmero de servidores
C = 10
# RO por servidor
RO = list(np.arange(1, 10, 1))
ARRIVAL_TIMES = [1/r for r in RO]

for i, arr_time in enumerate(ARRIVAL_TIMES):
    print(arr_time)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = LcfsMultiServerReassign(num_servers=C, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=50000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/multi_server_mm1_10sv/mm1_ro_" + str(RO[i]) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))
