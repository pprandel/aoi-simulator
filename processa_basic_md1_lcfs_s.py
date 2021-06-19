import numpy as np
from mean_aoi_lcfs import mean_aoi_lcfs

RO = list(np.arange(0.1, 2, 0.1))
ARRIVAL_TIMES = [1/r for r in RO]

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (np.exp(ro) / ro)

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    print("Processando mm1_ro_%s" %(str(ro)))
    path = "experimentos/md1_lcfs_s/md1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_lcfs(path)
    analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_md1_lcfs_s_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_md1_lcfs_s_aoi.txt", 'w') as f:
    f.write(str(analit_aoi))

