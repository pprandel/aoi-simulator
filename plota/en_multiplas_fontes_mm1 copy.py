import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf

file_analit = "resultados/analit_duas_fontes_mm1_aoi.txt"
file_sim = "resultados/sim_duas_fontes_mm1_aoi.txt"

with open (file_analit, 'r') as d:
    data_analit = json.load(d)
with open (file_sim, 'r') as d:
    data_sim = json.load(d)

fig, ax = plt.subplots()

def get_ages(ros_dic):
    ages = []
    for v in ros_dic.values():
        if v == Inf:
            v = 1000
        ages.append(v)
    return ages

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

c = 0
for ro, age_list in data_analit.items():
    x_analit = []
    y_analit = []
    x_sim = []
    y_sim = []
    for lista in age_list:
        ages = get_ages(lista)
        print(ages)
        x_analit.append(ages[0])
        y_analit.append(ages[1])
    for lista in data_sim[ro]:
        ages = get_ages(lista)
        print(ages)
        x_sim.append(ages[0])
        y_sim.append(ages[1])
    ax.plot(x_analit, y_analit, colors[c], marker='x', markersize=7, label=r"$\rho$= "+ro+" (analytical)")
    ax.plot(x_sim, y_sim, colors[c], marker='o', linestyle='--', markersize=7, label=r"$\rho$= "+ro+" (simulated)")
    c = c + 1

ax.set_xlabel('AoI of source 1', fontsize=20)
ax.set_ylabel('AoI of source 2', fontsize=20)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.legend(fontsize=16, loc='upper right', ncol=2) #,bbox_to_anchor=(0.5, -0.05))
ax.set_xlim(3, 20)
ax.set_ylim(3, 20)
ax.grid(True)
plt.show()