import numpy as np
from numpy.core.fromnumeric import mean
from mean_aoi import mean_aoi_n_fontes

RO = list(np.arange(0.1, 1, 0.1))
ARRIVAL_TIMES = [1/r for r in RO]

# def calc_analitic_aoi(ro, mu):
#     return (1/mu) * (1 + 1/(2*ro))

sim_aoi = {}
#analit_aoi = {}

for ro in RO:
    print("Processando mm1_ro_%s" %(str(ro)))
    path = "experimentos/duas_fontes/mm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_n_fontes(path, 2)
    #analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_duas_fontes_mm1_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

# with open("resultados/analit_dm1_lcfs_s_aoi.txt", 'w') as f:
#     f.write(str(analit_aoi))

