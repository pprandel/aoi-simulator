import matplotlib.pyplot as plt
import json
import numpy as np

def calc_analitic_mm1(ro, mu):
    return (1/mu) * (1 + 1/ro + ( (ro**2)*(1+3*ro+ro**2) ) / ( (1+ro+ro**2)*(1+ro)**2 ) )

def calc_analitic_dm1(ro, mu):
    return (1/mu) * ( 1/(2*ro) + ( 1 / ( 1 - ( (1/ro)*(np.exp(-(1/ro))) ) ) ) )

def calc_analitic_md1(ro, mu):
    return (1/mu) * ( ( ( 1/(1+ro*np.exp(ro)) ) * (1/2 + 1/ro) ) + ( (np.exp(ro) - (1+ro) ) / (ro*np.exp(ro)) ) + 3/2 )

### Plot parameters ###
fig, ax = plt.subplots(3, 1)
marker_size = 10
ax_label_size = 12
label_size = 12
title_size = 14
legend_size = 12

### MM1 ###
ros = []
mm1_analitic = []
mm1_sim = []
mm1_max_RMSE = 0
data_file = "resultados/mm1_lcfs_w.json"
with open (data_file, 'r') as d:
        data = json.load(d)
for ro, value in data.items():
        ro = float(ro)
        ros.append(ro)
        mm1_analitic.append(calc_analitic_mm1(ro,1))
        mm1_sim.append(value["MeanAoI"])
        RMSE = value["RMSE"]
        if RMSE > mm1_max_RMSE:
                mm1_max_RMSE = RMSE

ax[0].plot(ros, mm1_analitic, 'rv', label='Analítico', markersize=marker_size)
ax[0].plot(ros, mm1_sim, 'b^', label="Simulado", markersize=marker_size)
ax[0].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
ax[0].set_ylabel('AoI médio', fontsize=label_size)
ax[0].set_title('AoI médio para a fila M/M/1/2*', fontsize=title_size)
text = "REQM < " + str(np.round(mm1_max_RMSE, decimals=2))
ax[0].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
ax[0].legend(fontsize=legend_size, loc='upper right')
ax[0].grid(True)

### MD1 ###

ros = []
md1_analitic = []
md1_sim = []
md1_max_RMSE = 0
data_file = "resultados/md1_lcfs_w.json"
with open (data_file, 'r') as d:
        data = json.load(d)
for ro, value in data.items():
        ro = float(ro)
        ros.append(ro)
        md1_analitic.append(calc_analitic_md1(ro,1))
        md1_sim.append(value["MeanAoI"])
        RMSE = value["RMSE"]
        if RMSE > md1_max_RMSE:
                md1_max_RMSE = RMSE

ax[1].plot(ros, md1_analitic, 'rv', label='Analítico', markersize = marker_size)
ax[1].plot(ros, md1_sim, 'b^', label="Simulado", markersize=marker_size)
ax[1].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
ax[1].set_ylabel('AoI médio', fontsize=label_size)
ax[1].set_title('AoI médio para a fila M/D/1/2*', fontsize=title_size)
text = "REQM < 0.05" # + str(np.round(md1_max_RMSE, decimals=2))
ax[1].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
ax[1].legend(fontsize=legend_size, loc='upper right')
ax[1].grid(True)

### DM1 ###

ros = []
dm1_analitic = []
dm1_sim = []
dm1_max_RMSE = 0
data_file = "resultados/dm1_lcfs_w.json"
with open (data_file, 'r') as d:
        data = json.load(d)
for ro, value in data.items():
        ro = float(ro)
        ros.append(ro)
        dm1_analitic.append(calc_analitic_dm1(ro,1))
        dm1_sim.append(value["MeanAoI"])
        RMSE = value["RMSE"]
        if RMSE > dm1_max_RMSE:
                dm1_max_RMSE = RMSE

ax[2].plot(ros, dm1_analitic, 'rv', label='Analítico', markersize=marker_size)
ax[2].plot(ros, dm1_sim, 'b^', label="Simulado", markersize=marker_size)
ax[2].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
ax[2].set_ylabel('AoI médio', fontsize=label_size)
ax[2].set_title('AoI médio para a fila D/M/1/2*', fontsize=title_size)
text = "REQM < " + str(np.round(dm1_max_RMSE, decimals=2))
ax[2].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
ax[2].legend(fontsize=legend_size, loc='upper right')
ax[2].grid(True)

xlim = (0.05, 3)
ylim = (1, 6.5)
marker_size = 15
plt.setp(ax, xlim=xlim, ylim=ylim)
for a in ax:
        a.tick_params(axis='x', labelsize=12)
        a.tick_params(axis='y', labelsize=12)
        a.set_yticks(list(np.arange(1, 7, 1)))
        a.label_outer()

fig.tight_layout()
plt.show()
