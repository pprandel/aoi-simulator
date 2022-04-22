import json
import matplotlib.pyplot as plt
from numpy import Infinity
import numpy as np

# Cáclulo dos valores analíticos
def calc_analitic_aoi(ro_0, ro_1, mu):
    def calc_age(ro_i, ro_menos_i, mu):
        ro = ro_i + ro_menos_i
        return (1/mu) * ( (ro_i**2 * (1-ro*ro_menos_i)) / ((1-ro)*(1-ro_menos_i)**3) + 1/(1-ro_menos_i) + 1/ro_i )
    aoi = {}
    if ro_0 == 0:
        aoi[0] = 1000
    else:
        aoi[0] = calc_age(ro_0, ro_1, mu)
    if ro_1 == 0:
        aoi[1] = 1000
    else:
        aoi[1] = calc_age(ro_1, ro_0, mu)
    return aoi

### Parâmetros da figura ###
fig, ax = plt.subplots()

# Carregamos os resultados da simulação
# A pasta resultados deve estar no mesmo diretório deste script
data_file = "resultados/exemplo_3.json"
with open (data_file, 'r') as d:
    data = json.load(d)

def get_ages(dic):
    ages = []
    rmse = []
    for v1 in dic.values():
        v = v1["MeanAoI"]
        if v == Infinity:
            v = 1000
        ages.append(v)
        rmse.append(v1["RMSE"])
    return (ages,rmse)

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
# Erro máximo
max_rmse = 0
for ro, v1 in data.items():
    x_analit = []
    y_analit = []
    x_sim = []
    y_sim = []
    for k, v2 in v1.items():
        ros = k.split("_")
        ro_1 = float(ros[0])
        ro_2 = float(ros[1])
        # Recupera os valores da simulação
        sim = get_ages(v2)
        x_sim.append(sim[0][0])
        y_sim.append(sim[0][1])
        rmse = max(sim[1])
        if rmse > max_rmse:
            max_rmse = rmse
        # Calcula os valores analíticos
        analit = calc_analitic_aoi(ro_1, ro_2, 1)
        x_analit.append(analit[0])
        y_analit.append(analit[1])
    # Plotamos os valores simulados
    ax.plot(x_sim, y_sim, colors[c], marker='o', linestyle='--', markersize=7, label=r"$\rho$= " + str(ro) + " sim")
    # Plotamos os valores exatos
    ax.plot(x_analit, y_analit, colors[c], marker='x', linestyle='-', markersize=7, label=r"$\rho$= " + str(ro) + " exato")
    # Imprime o erro máximo
    text = "REQM < " + str(np.round(max_rmse, decimals=2))
    ax.text(23, 23, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
    c = c + 1
ax.set_xlabel('Age da fonte 1', fontsize=16)
ax.set_ylabel('Age da fonte 2', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=10, loc='lower right')
ax.set_xlim(0, 25)
ax.set_ylim(0, 25)
ax.grid(True)
plt.show()