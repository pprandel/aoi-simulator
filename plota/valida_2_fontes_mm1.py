import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np

def calc_analitic_aoi(ro_0, ro_1, mu):
    def calc_age(ro_i, ro_menos_i, mu):
        ro = ro_i + ro_menos_i
        return (1/mu) * ( (ro_i**2 * (1-ro*ro_menos_i)) / ((1-ro)*(1-ro_menos_i)**3) + 1/(1-ro_menos_i) + 1/ro_i )
    aoi = {}
    aoi[0] = calc_age(ro_0, ro_1, mu)
    aoi[1] = calc_age(ro_1, ro_0, mu)
    return aoi

def mirror_list(l,m):
    N = len(l)
    for i in range (N-1):
        l.append(m[N-2-i])
        m.append(l[N-2-i])
    return

fig, ax = plt.subplots()

colors = ['#1f77b4',
          '#ff7f0e',
          '#2ca02c',
          '#d62728',
          '#9467bd',
          '#8c564b',
          '#e377c2',
          '#7f7f7f',
          '#bcbd22',
          '#17becf',
          '#1a55FF']

# Init color
c = 0

# Load data
data_file = "resultados/mm1_2_sources.json"

with open (data_file, 'r') as d:
    data = json.load(d)

max_RMSE = 0
for key, value in data.items():
    ro = key
    x_analit = []
    y_analit = []
    x_sim = []
    y_sim = []
    for k, v in value.items():
        ros = k.split("_")
        ro_1 = float(ros[1])
        ro_2 = float(ros[2])
        ages = v
        x_sim.append(ages["0"]["MeanAoI"])
        RMSE1 = ages["0"]["RMSE"]
        if RMSE1 > max_RMSE:
            max_RMSE = RMSE1
        y_sim.append(ages["1"]["MeanAoI"])
        RMSE2 = ages["1"]["RMSE"]
        if RMSE2 > max_RMSE:
            max_RMSE = RMSE2
        analit = calc_analitic_aoi(ro_1, ro_2, 1)
        x_analit.append(analit[0])
        y_analit.append(analit[1])
    mirror_list(x_sim, y_sim)    
    mirror_list(x_analit, y_analit)
    ax.plot(x_analit, y_analit, colors[c], marker='x', markersize=7, label=r"$\rho$= "+ro+" analítico")
    ax.plot(x_sim, y_sim, colors[c], marker='o', linestyle='--', markersize=7, label=r"$\rho$= "+ro+" simulado")
    c = c + 1

ax.set_xlabel('Age da fonte 1', fontsize=16)
ax.set_ylabel('Age da fonte 2', fontsize=16)
text = "REQM < " + str(np.round(max_RMSE, decimals=2))
ax.text(8, 10, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='upper right')
ax.set_xlim(3, 15)
ax.set_ylim(3, 15)
ax.grid(True)
plt.show()