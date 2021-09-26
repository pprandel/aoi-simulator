import queueing_tool as qt
import numpy as np


RO = 0.9
arr_time = 1/RO

mean_delay = {}

for i in range(1,20):
    print(i)
    def arr(t): return t+ np.random.exponential(arr_time)
    def ser(t): return t + np.random.exponential(1)
    q = qt.QueueServer(1, arrival_f=arr, service_f=ser)
    q.clear()
    q.set_active()
    q.collect_data = True
    q.simulate(n=10000, nD=10000)
    num_events = q.num_arrivals[0] + q.num_departures
    data = q.data
    arq_nome = "experimentos/mm1_multi/" + str(i) + ".txt"
    with open(arq_nome, 'w') as f:
        f.write(str(data))
