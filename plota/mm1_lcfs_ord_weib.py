import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/mm1_lcfs_ord__weib_s.json", "resultados/mm1_lcfs_ord__weib_w.json", 
"resultados/mm1_lcfs_ord__weib_c.json"]

data = [[],[],[]]
ro = [[],[],[]]
aoi = [[],[],[]]
for i, file in enumerate(data_files):
        with open (file, 'r') as d:
                data[i] = json.load(d)

        for key, value in data[i].items():
                ro[i].append(float(key))
                aoi[i].append(value["MeanAoI"])
        print(aoi[i])

tam_linha = 2
tam_marker = 7
ax.plot(ro[0], aoi[0], 'or-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-S")
ax.plot(ro[1], aoi[1], '^b-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-W")
ax.plot(ro[2], aoi[2], 'vg-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-C")

ax.set_ylabel('Age média', fontsize=14)
ax.set_xlabel(r'Carga no servidor $(\rho)$', fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='upper center')
ax.set_xlim(0.4, 5)
ax.set_ylim(1.3, 3.4)
ax.set_yticks(list(np.arange(1.3, 3.5, 0.3)))
ax.set_xticks(list(np.arange(0, 5, 0.5)))
ax.grid(True)
plt.show()