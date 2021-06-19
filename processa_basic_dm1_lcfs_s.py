import numpy as np
from mean_aoi_lcfs import mean_aoi_lcfs

RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/r for r in RO]

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/(2*ro))

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    print("Processando dm1_ro_%s" %(str(ro)))
    path = "experimentos/dm1_lcfs_s/dm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_lcfs(path)
    analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_dm1_lcfs_s_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_dm1_lcfs_s_aoi.txt", 'w') as f:
    f.write(str(analit_aoi))

