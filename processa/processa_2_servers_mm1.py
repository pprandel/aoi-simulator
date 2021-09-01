import numpy as np
from mean_aoi import mean_aoi

C = 1
RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/(r*C) for r in RO]

# def calc_analitic_aoi(ro, mu):
#     lamb = ro*mu*C/2
#     return 1/(2*mu) + 1/(2*lamb) + (1/(2*mu)) * (1/(2*lamb)) * ( mu*lamb/(lamb+mu) + mu*lamb/(lamb+mu) )
sim_aoi = {}
# analit_aoi = {}

for ro in RO:
    print("Processando para ro = %s" %(ro))
    path = "experimentos/2_servers_mm1/mm1_ro_" + str(ro) + ".txt"
    sim_aoi[ro] = mean_aoi(path)
    # analit_aoi[ro] = calc_analitic_aoi(ro, 1)

with open("resultados/sim_mm1_aoi.txt", 'w') as f:
    f.write(str(sim_aoi))

# with open("resultados/analit_2_servers_mm1_aoi.txt", 'w') as f:
#     f.write(str(analit_aoi))

