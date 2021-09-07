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

ro = 0.7
ro_0 = 0.21
ro_1 = 0.49
print("ro_0: %f ro_1: %f " %(ro_0, ro_1))
arq_nome = "experimentos/duas_fontes/mm1/ro_" + str(ro) + "_" + str(ro_0) + "_" + str(ro_1) + ".txt"
sim_aoi = mean_aoi_n_fontes(arq_nome, 2)
analit_aoi = calc_analitic_aoi(ro_0, ro_1, 1)

print("Simulado")
print(sim_aoi)
print("Analitico")
print(analit_aoi)