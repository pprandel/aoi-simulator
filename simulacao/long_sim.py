import queueing_tool as qt
import numpy as np
from LcfsPreemption import LcfsPreemption

#RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ro = 0.5
# ARRIVAL_TIMES = [1/r for r in RO]
arr_time = 1/ro

def arr(t): return t+ np.random.exponential(arr_time)
def ser(t): return t + np.random.exponential(1)
q = qt.QueueServer(arrival_f=arr, service_f=ser)


q.clear()
q.set_active()
q.collect_data = True
q.simulate(n=100000, nD=100000)
num_events = q.num_arrivals[0] + q.num_departures
data = q.data
arq_nome = "experimentos/long_sim.txt"
with open(arq_nome, 'w') as f:
    f.write(str(data))
