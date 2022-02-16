import json
from turtle import color
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots(2,1)

# Load data
data_files = ["resultados/mm1_lcfs_no_ord__ln_s.json", "resultados/mm1_lcfs_no_ord__ln_w.json", 
"resultados/mm1_lcfs_no_ord__ln_c.json"]

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
ax[0].plot(ro[0], aoi[0], 'or-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-S")
ax[0].plot(ro[1], aoi[1], '^b-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-W")
ax[0].plot(ro[2], aoi[2], 'vg-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-C")

width = 0.05  # the width of the bars

ax[1].bar([ro-width for ro in ro[0]], preemp[0], width, color='r', label="LGFS-S")
ax[1].bar(ro[1], preemp[1], width, color='b', label="LGFS-W")
ax[1].bar([ro+width for ro in ro[2]], preemp[2], width, color='g', label="LGFS-C")

ax[0].set_title('A')
ax[1].set_title('B')
ax[0].set_ylabel('Age média', fontsize=14)
ax[1].set_ylabel('Pacotes descartados', fontsize=14)
ax[1].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=14)
ax[0].yaxis.tick_right()
ax[1].yaxis.tick_right()

ax[0].tick_params(axis='x', labelsize=12)
ax[1].tick_params(axis='x', labelsize=12)
ax[0].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='y', labelsize=12)
ax[0].legend(fontsize=12, loc='upper right')

ax[0].set_xlim(0.3, 3.1)
ax[1].set_xlim(0.3, 3.1)
ax[0].set_ylim(2.3, 5.5)
ax[0].set_yticks(list(np.arange(2.3, 5.5, 0.7)))
ax[0].set_xticks(list(np.arange(0.4, 3.1, 0.4)))
ax[1].set_xticks(list(np.arange(0.4, 3.1, 0.4)))
ax[0].grid(True)
ax[1].grid(True)
plt.show()