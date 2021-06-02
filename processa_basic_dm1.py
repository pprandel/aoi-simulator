import numpy as np
from mean_aoi import mean_aoi
from scipy.special import lambertw

RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/r for r in RO]

def beta(ro):
    return -ro * lambertw( -1/ro * np.exp(-1/ro) )

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1/(2*ro) + 1/(1-beta(ro)) )

sim_aoi = {}
analit_aoi = {}

for ro in RO:
    path = "experimentos/dm1/dm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi(path)
    analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_dm1_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

with open("resultados/analit_dm1_aoi.txt", 'w') as f:
    f.write(str(analit_aoi))

