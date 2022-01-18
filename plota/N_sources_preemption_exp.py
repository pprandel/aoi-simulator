import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/N_sources_preemption_exp_lgfs.json", "resultados/N_sources_preemption_exp_max.json", 
"resultados/N_sources_preemption_exp_masif.json"]

data = [[],[],[]]
ro = [[],[],[]]
aoi = [[],[],[]]
for i, file in enumerate(data_files):
        with open (file, 'r') as d:
                data[i] = json.load(d)

        for key, value in data[i].items():
                ro[i].append(float(key))
                aoi[i].append(value)
        print(aoi[i])
ax.plot(ro[0], aoi[0], 'ro', markersize=7, label="LGFS")
ax.plot(ro[1], aoi[1], 'b^', markersize=7, label="LGFS-MAX")
ax.plot(ro[2], aoi[2], 'gv', markersize=7, label="LGFS-MASIF")

      
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='upper right')
ax.set_title('AoI médio N=50 M=3 / precedência / sv exp', fontsize=16)
# ax.set_xlim(3, 15)
# ax.set_ylim(3, 15)
ax.grid(True)
plt.show()