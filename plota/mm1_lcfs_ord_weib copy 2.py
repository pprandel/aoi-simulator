import json
import matplotlib.pyplot as plt
from numpy.core.numeric import Inf
import numpy as np


fig, ax = plt.subplots()

# Load data
data_files = ["resultados/mm1_lcfs_ord__ln_s.json", "resultados/mm1_lcfs_ord__ln_w.json", 
"resultados/mm1_lcfs_ord__ln_c.json"]

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
# ax.plot(ro[0], aoi[0], 'or-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-S")
# ax.plot(ro[1], aoi[1], '^b-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-W")
# ax.plot(ro[2], aoi[2], 'vg-', linewidth=tam_linha, markersize=tam_marker, label="LGFS-C")

width = 0.35  # the width of the bars

ax.bar(ro[0], preemp[0], width, label="LGFS-S")
ax.bar(ro[1], preemp[1], width, label="LGFS-W")
ax.bar(ro[2], preemp[2], width, label="LGFS-C")


ax.set_ylabel('Age média', fontsize=14)
ax.set_xlabel(r'Carga no servidor $(\rho)$', fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=14, loc='upper center')
# ax.set_xlim(0.4, 5)
# ax.set_ylim(1.3, 3.4)
# ax.set_yticks(list(np.arange(1.3, 3.5, 0.3)))
# ax.set_xticks(list(np.arange(0, 5, 0.5)))
ax.grid(True)
plt.show()



import matplotlib.pyplot as plt
import numpy as np

labels = ['G1', 'G2', 'G3', 'G4', 'G5']
men_means = [20, 34, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects2 = ax.bar(x + width/2, women_means, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()