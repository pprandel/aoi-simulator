import json
from turtle import color
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/mm1_lcfs_no_ord__exp_s.json", "resultados/mm1_lcfs_no_ord__exp_w.json", 
"resultados/mm1_lcfs_no_ord__exp_c.json"]

data = [[],[],[]]
ro = [[],[],[]]
aoi = [[],[],[]]
preemp = [[],[],[]]
for i, file in enumerate(data_files):
        with open (file, 'r') as d:
                data[i] = json.load(d)

        for key, value in data[i].items():
                ro[i].append(float(key))
                aoi[i].append(value["MeanAoI"])
                preemp[i].append(value["Preempted"])
        print(aoi[i])

tam_linha = 2
tam_marker = 7
ax.plot(ro[0], aoi[0], 'or-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-S")
ax.plot(ro[1], aoi[1], '^b-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-W")
ax.plot(ro[2], aoi[2], 'vg-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-C")



ax.set_ylabel('Age média', fontsize=14)
ax.yaxis.tick_right()

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=12, loc='upper right')

ax.set_xlim(0.3, 3.1)
ax.set_ylim(1.5, 4)
ax.set_yticks(list(np.arange(1.5, 4.1, 0.5)))
ax.set_xticks(list(np.arange(0.4, 3.1, 0.4)))
ax.grid(True)
plt.show()