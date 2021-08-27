import numpy as np
from mean_aoi import mean_aoi
import matplotlib.pyplot as plt

ro = 0.9
arr_time = 1/ro

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

sim_aoi = []
analit_aoi = {}

for i in range(1,20):
    print("Processando para i = %s" %(i))
    path = "experimentos/mm1_multi/" + str(i) + ".txt"
    sim_aoi.append(mean_aoi(path))
analit_aoi = calc_analitic_aoi(ro, 1)
print("AoI analítico: %f" %(analit_aoi))
print("AoI simulado: %f" %(np.mean(sim_aoi)))
print("Variância: %f" %(np.var(sim_aoi)))
plt.hist(sim_aoi, bins='auto')
plt.show()