import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf

file_sim = "resultados/sim_duas_fontes_dm1_aoi.txt"

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
for ro, age_list in data_sim.items():
    x_sim = []
    y_sim = []
    for lista in data_sim[ro]:
        ages = get_ages(lista)
        print(ages)
        x_sim.append(ages[0])
        y_sim.append(ages[1])
    ax.plot(x_sim, y_sim, colors[c], marker='o', linestyle='--', markersize=7, label=r"$\rho$= "+ro+" simulado")
    c = c + 1

ax.set_xlabel('Age da fonte 1', fontsize=16)
ax.set_ylabel('Age da fonte 2', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='lower left')
ax.set_xlim(0, 15)
ax.set_ylim(0, 15)
ax.grid(True)
plt.show()