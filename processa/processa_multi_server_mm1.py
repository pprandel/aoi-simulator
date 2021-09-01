import numpy as np
from mean_aoi import mean_aoi_lcfs


# Nmero de servidores
C = 10
# RO total
RO = list(np.arange(1, 10, 1))

def calc_analitic_aoi(ro, mu, C):
    def prod_2(l):
        prod_2 = 1
        for i in range(l):
            prod_2 = prod_2 * (ro / (i+1+ro))
        return prod_2
    prod_1 = 1
    for i in range(C-1):
        prod_1 = prod_1 * (ro / (i+1+ro))
    sum = 0
    for l in range(C-1):
        sum = sum + prod_2(l+1)
    return ( (1/mu) * ((1/C) * prod_1 + 1/ro + (1/ro) * sum) )

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    print("Processando para ro = %s" %(ro))
    path = "experimentos/multi_server_mm1_10sv/mm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_lcfs(path)
    analit_aoi[ro] = calc_analitic_aoi(ro, 1, C)

with open("resultados/sim_multi_server_10sv.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_multi_server_10sv.txt", 'w') as f:
    f.write(str(analit_aoi))

