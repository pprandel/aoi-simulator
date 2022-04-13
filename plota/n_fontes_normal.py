import matplotlib.pyplot as plt
import json
import numpy as np

fig, ax = plt.subplots()

# Load data
data_file = "resultados/dissertacao_lcfs_c_lgfs_mw.json"

x = []
m_aoi = []
m_p_aoi = []

with open (data_file, 'r') as d:
        data = json.load(d)

for key, value in data.items():
    x.append(int(key))
    m_aoi.append(value["MeanAoI"])
    m_p_aoi.append(value["MeanPeakAoI"])

tam_linha = 2
tam_marker = 7
ax.plot(x, m_aoi, '-', color='indigo', linewidth=tam_linha, markersize=tam_marker, label="AoI médio")
ax.plot(x, m_p_aoi, '-', color='tomato', linewidth=tam_linha, markersize=tam_marker, label="AoI de pico médio")

data_file = "resultados/dissertacao_sem_tecnicas.json"

x = []
m_aoi = []
m_p_aoi = []

with open (data_file, 'r') as d:
        data = json.load(d)

for key, value in data.items():
    x.append(int(key))
    m_aoi.append(value["MeanAoI"])
    m_p_aoi.append(value["MeanPeakAoI"])

tam_linha = 2
tam_marker = 7
ax.plot(x, m_aoi, '-', color='blue', linewidth=tam_linha, markersize=tam_marker, label="AoI médio")
ax.plot(x, m_p_aoi, '-', color='green', linewidth=tam_linha, markersize=tam_marker, label="AoI de pico médio")

# ax.axhline(y=15, color='indigo', linestyle='--', label="Limite AoI médio")
# ax.axhline(y=20, color='tomato', linestyle='--', label="Limite AoI de pico médio")

# ax.axhline(y=10, color='orange', linestyle='--')
# ax.axhline(y=15, color='orange', linestyle=':')

# ax.axhline(y=20, color='green', linestyle='--')
# ax.axhline(y=30, color='green', linestyle=':')

ax.set_xticks(list(np.arange(30, 151, 10)))

ax.set_ylabel('AoI (segundos)', fontsize=14)
ax.set_xlabel('Número de agentes alocados', fontsize=14)

ax.grid(True)
ax.legend(fontsize=12, loc='upper left')
#ax.text(2000, 3.25, r'Analytical value ($\gamma=3.5$)', ha='left', va='center',fontsize=14, color='indigo')

plt.show()