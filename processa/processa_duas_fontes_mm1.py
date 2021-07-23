import numpy as np
from numpy.core.fromnumeric import mean
from mean_aoi import mean_aoi_n_fontes
import json

def calc_analitic_aoi(ro_0, ro_1, mu):
    def calc_age(ro_i, ro_menos_i, mu):
        ro = ro_i + ro_menos_i
        return (1/mu) * ( (ro_i**2 * (1-ro*ro_menos_i)) / ((1-ro)*(1-ro_menos_i)**3) + 1/(1-ro_menos_i) + 1/ro_i )
    aoi = {}
    aoi[0] = calc_age(ro_0, ro_1, mu)
    aoi[1] = calc_age(ro_1, ro_0, mu)
    return aoi

sim_aoi = {}
analit_aoi = {}

RO = list(np.arange(0.1, 1, 0.1))
RO = [round(ro,2) for ro in RO]
for ro in RO:
    ro_str = str(ro)
    analit_aoi[ro_str] = []
    sim_aoi[ro_str] = []
    # ro das fontes
    print("Processando para ro: %f" %ro)
    for percent in np.arange(0, 1.1, 0.1):
        ro_0 = round(ro*percent, 2)
        ro_1 = round(ro - ro_0, 2)
        print("ro_0: %f ro_1: %f " %(ro_0, ro_1))
        arq_nome = "experimentos/duas_fontes/mm1/ro_" + str(ro) + "_" + str(ro_0) + "_" + str(ro_1) + ".txt"
        sim_aoi[ro_str].append(mean_aoi_n_fontes(arq_nome, 2))
        analit_aoi[ro_str].append(calc_analitic_aoi(ro_0, ro_1, 1))

with open("resultados/sim_duas_fontes_mm1_aoi.txt", 'w') as f:
    json.dump(sim_aoi, f, indent=2)

with open("resultados/analit_duas_fontes_mm1_aoi.txt", 'w') as f:
    json.dump(analit_aoi, f, indent=2)