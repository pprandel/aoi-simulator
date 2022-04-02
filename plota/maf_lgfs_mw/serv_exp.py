import json
from turtle import color
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/maf_lgfs_mw_preemption_exp.json", "resultados/maf_lgfs_preemption_exp.json", 
"resultados/masif_lgfs_no_preemption_exp.json", "resultados/normal_lgfs_preemption_exp.json"]

data = [[],[],[],[]]
ro = [[],[],[],[]]
aoi = [[],[],[],[]]
for i, file in enumerate(data_files):
        with open (file, 'r') as d:
                data[i] = json.load(d)

        for key, value in data[i].items():
                ro[i].append(float(key))
                aoi[i].append(value)
        print(aoi[i])

tam_linha = 2
tam_marker = 7
ax.plot(ro[0], aoi[0], 'or-', linewidth=tam_linha, markersize=tam_marker, label="MAF-LGFS-MW")
ax.plot(ro[1], aoi[1], 'ob-', linewidth=tam_linha, markersize=tam_marker, label="MAF-LGFS-S")
ax.plot(ro[3], aoi[3], 'oy-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-S")
ax.plot(ro[2], aoi[2], '^g-', linewidth=tam_linha, markersize=tam_marker, label="MASIF-LGFS (s/ preemp.)")


ax.set_ylabel('AoI média', fontsize=14)
ax.set_xlabel(r'Carga total $(\rho)$', fontsize=14)
ax.yaxis.tick_right()

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=12, loc='upper right')

ax.set_xlim(0.1, 3.1)
ax.set_ylim(1.5, 20)
# ax.set_yticks(list(np.arange(1.5, 4.1, 0.5)))
# ax.set_xticks(list(np.arange(0.4, 3.1, 0.4)))
ax.grid(True)
plt.show()