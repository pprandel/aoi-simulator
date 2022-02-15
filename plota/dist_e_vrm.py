import matplotlib.pyplot as plt
import json
import numpy as np
from reliability.Distributions import Exponential_Distribution as EXP
from reliability.Distributions import Weibull_Distribution as WEI
from reliability.Distributions import Lognormal_Distribution as LOG

### Plot parameters ###
fig = plt.figure(constrained_layout=True)
subfigs = fig.subfigures(nrows=3, ncols=1)

subfigs[0].suptitle = 'Exponencial'
subfigs[1].suptitle = 'Weibull'
subfigs[2].suptitle = 'Lognormal'

ax = []
for row, subfig in enumerate(subfigs):
    ax[0] = subfigs.subplots(1, 2)

marker_size = 5
ax_label_size = 12
label_size = 12
title_size = 14
legend_size = 12

x = np.arange(0, 5, 0.01)

exp = EXP(Lambda=1)
y_exp = exp.PDF(xvals=x, show_plot=False)
vrm_exp = {}
for i in x:
    vrm_exp[np.round(i,2)] = np.round(exp.mean_residual_life(i), 3)

wei = WEI(1,2)
y_wei = wei.PDF(xvals=x, show_plot=False)
vrm_wei = {}
for i in x:
    vrm_wei[np.round(i,2)] = np.round(wei.mean_residual_life(i), 3)

log = LOG(0.2,0.5)
y_log = log.PDF(xvals=x, show_plot=False)
vrm_log = {}
for i in x:
    vrm_log[np.round(i,2)] = np.round(log.mean_residual_life(i), 3)


ax[0][0].plot(x, y_exp, 'r', label='Exponencial', markersize=marker_size)
ax[0][0].set_title('Exponencial')
ax[0][1].plot(vrm_exp.keys(), vrm_exp.values(), 'r', label='VRM', markersize=marker_size)
ax[1][0].plot(x, y_wei, 'r', label='Weibull', markersize=marker_size)
ax[1][0].set_title('Weibull')
ax[1][1].plot(vrm_wei.keys(), vrm_wei.values(), 'r', label='VRM', markersize=marker_size)
ax[2][0].plot(x, y_log, 'r', label='Lognormal', markersize=marker_size)
ax[2][0].set_title('Lognormal')
ax[2][1].plot(vrm_log.keys(), vrm_log.values(), 'r', label='VRM', markersize=marker_size)



plt.show()

# ax[0].plot(ros, mm1_sim, 'b^', label="Simulado", markersize=marker_size)
# ax[0].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
# ax[0].set_ylabel('AoI médio', fontsize=label_size)
# ax[0].set_title('AoI médio para a fila M/M/1/1*', fontsize=title_size)
# text = "REQM < " + str(np.round(mm1_max_RMSE, decimals=2))
# ax[0].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
# ax[0].legend(fontsize=legend_size, loc='upper right')
# ax[0].grid(True)

# ### MD1 ###

# ros = []
# md1_analitic = []
# md1_sim = []
# md1_max_RMSE = 0
# data_file = "resultados/md1_lcfs_s.json"
# with open (data_file, 'r') as d:
#         data = json.load(d)
# for ro, value in data.items():
#         ro = float(ro)
#         ros.append(ro)
#         md1_analitic.append(calc_analitic_md1(ro,1))
#         md1_sim.append(value["MeanAoI"])
#         RMSE = value["RMSE"]
#         if RMSE > md1_max_RMSE:
#                 md1_max_RMSE = RMSE

# ax[1].plot(ros, md1_analitic, 'rv', label='Analítico', markersize = marker_size)
# ax[1].plot(ros, md1_sim, 'b^', label="Simulado", markersize=marker_size)
# ax[1].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
# ax[1].set_ylabel('AoI médio', fontsize=label_size)
# ax[1].set_title('AoI médio para a fila M/D/1/1*', fontsize=title_size)
# text = "REQM < 0.05" # + str(np.round(md1_max_RMSE, decimals=2))
# ax[1].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
# ax[1].legend(fontsize=legend_size, loc='lower right')
# ax[1].grid(True)

# ### DM1 ###

# ros = []
# dm1_analitic = []
# dm1_sim = []
# dm1_max_RMSE = 0
# data_file = "resultados/dm1_lcfs_s.json"
# with open (data_file, 'r') as d:
#         data = json.load(d)
# for ro, value in data.items():
#         ro = float(ro)
#         ros.append(ro)
#         dm1_analitic.append(calc_analitic_dm1(ro,1))
#         dm1_sim.append(value["MeanAoI"])
#         RMSE = value["RMSE"]
#         if RMSE > dm1_max_RMSE:
#                 dm1_max_RMSE = RMSE

# ax[2].plot(ros, dm1_analitic, 'rv', label='Analítico', markersize=marker_size)
# ax[2].plot(ros, dm1_sim, 'b^', label="Simulado", markersize=marker_size)
# ax[2].set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
# ax[2].set_ylabel('AoI médio', fontsize=label_size)
# ax[2].set_title('AoI médio para a fila D/M/1/1*', fontsize=title_size)
# text = "REQM < " + str(np.round(dm1_max_RMSE, decimals=2))
# ax[2].text(1.5, 5, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
# ax[2].legend(fontsize=legend_size, loc='upper right')
# ax[2].grid(True)

# xlim = (0.05, 3)
# ylim = (0.5, 6.5)
# marker_size = 15
# plt.setp(ax, xlim=xlim, ylim=ylim)
# for a in ax:
#         a.tick_params(axis='x', labelsize=12)
#         a.tick_params(axis='y', labelsize=12)
#         a.set_yticks(list(np.arange(0, 7, 1)))
#         a.label_outer()

# fig.tight_layout()
# plt.show()
