import numpy as np
from mean_aoi_lcfs import mean_aoi_lcfs

RO = list(np.arange(0.1, 2, 0.1))
ARRIVAL_TIMES = [1/r for r in RO]

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + ( (ro**2)*(1+3*ro+ro**2) ) / ( (1+ro+ro**2)*(1+ro)**2 ) )

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    print("Processando mm1_ro_%s" %(str(ro)))
    path = "experimentos/mm1_lcfs_w/mm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_lcfs(path)
    analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_mm1_lcfs_w_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_mm1_lcfs_w_aoi.txt", 'w') as f:
    f.write(str(analit_aoi))

