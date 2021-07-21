import numpy as np
from numpy.core.fromnumeric import mean
from mean_aoi import mean_aoi_n_fontes

RO = list(np.arange(0.1, 1, 0.1))
ARRIVAL_TIMES = [2/r for r in RO]

def calc_analitic_aoi(ro_1, ro_2, mu):
    def calc_age(ro_i, ro_menos_i, mu):
        ro = ro_i + ro_menos_i
        return (1/mu) * ( (ro_i**2 * (1-ro*ro_menos_i)) / ((1-ro)*(1-ro_menos_i)**3) + 1/(1-ro_menos_i) + 1/ro_i )
    age_1 = calc_age(ro_1, ro_2, mu)
    age_2 = calc_age(ro_2, ro_1, mu)
    return (age_1, age_2)

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    print("Processando mm1_ro_%s" %(str(ro)))
    path = "experimentos/duas_fontes/mm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi_n_fontes(path, 2)
    analit_aoi[ro] = calc_analitic_aoi(ro/2, ro/2, 1)

with open("resultados/sim_duas_fontes_mm1_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_duas_fontes_mm1_aoi.txt", 'w') as f:
    f.write(str(analit_aoi))

