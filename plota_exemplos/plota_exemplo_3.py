import json
import matplotlib.pyplot as plt
from numpy import Infinity
from numpy.core.numeric import Inf

### Parâmetros da figura ###
fig, ax = plt.subplots()

# Carregamos os resultados da simulação
# A pasta resultados deve estar no mesmo diretório deste script
data_file = "resultados/exemplo_3.json"
with open (data_file, 'r') as d:
    data = json.load(d)

def get_ages(dic):
    ages = []
    for v in dic.values():
        if v["MeanAoI"] == Infinity:
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
for ro, v1 in data.items():
    x = []
    y = []
    for v2 in v1.values():
        ages = get_ages(v2)
        x.append(ages[0])
        y.append(ages[1])
    ax.plot(x, y, colors[c], marker='o', linestyle='--', markersize=7) #, label=r"$\rho$= " + str(ro))
    c = c + 1

ax.set_xlabel('Age da fonte 1', fontsize=16)
ax.set_ylabel('Age da fonte 2', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='lower left')
ax.set_xlim(0, 30)
ax.set_ylim(0, 30)
ax.grid(True)
plt.show()