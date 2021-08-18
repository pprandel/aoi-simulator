import numpy as np
from numpy.core.fromnumeric import mean
from mean_aoi import mean_aoi_n_fontes
import json

sim_aoi = {}

RO = list(np.arange(0.1, 1, 0.1))
RO = [round(ro,2) for ro in RO]
for ro in RO:
    ro_str = str(ro)
    sim_aoi[ro_str] = []
    # ro das fontes
    print("Processando para ro: %f" %ro)
    for percent in np.arange(0, 1.1, 0.1):
        ro_0 = round(ro*percent, 2)
        ro_1 = round(ro - ro_0, 2)
        print("ro_0: %f ro_1: %f " %(ro_0, ro_1))
        arq_nome = "experimentos/duas_fontes/dm1/ro_" + str(ro) + "_" + str(ro_0) + "_" + str(ro_1) + ".txt"
        sim_aoi[ro_str].append(mean_aoi_n_fontes(arq_nome, 2))

with open("resultados/sim_duas_fontes_dm1_aoi.txt", 'w') as f:
    json.dump(sim_aoi, f, indent=2)