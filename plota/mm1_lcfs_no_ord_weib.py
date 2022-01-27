import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/mm1_lcfs_no_ord__weib_s.json", "resultados/mm1_lcfs_no_ord__weib_w.json", 
"resultados/mm1_lcfs_no_ord__weib_c.json"]

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
ax.plot(ro[0], aoi[0], 'r-', label="S")
ax.plot(ro[1], aoi[1], 'b-.', label="W")
ax.plot(ro[2], aoi[2], 'g--', label="C")

      
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='upper right')
ax.set_title('Comparativo', fontsize=16)
# ax.set_xlim(3, 15)
# ax.set_ylim(3, 15)
ax.grid(True)
plt.show()