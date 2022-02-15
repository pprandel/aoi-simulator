import matplotlib.pyplot as plt
import json
import numpy as np
from reliability.Distributions import Exponential_Distribution as EXP
from reliability.Distributions import Weibull_Distribution as WEI
from reliability.Distributions import Lognormal_Distribution as LOG



### Plot parameters ###
suptitle_size = 14
marker_size = 5

fig = plt.figure(layout='constrained')
subfigs = fig.subfigures(nrows=3, ncols=1, hspace=0.1)

subfigs[0].suptitle('Exponencial', fontsize=suptitle_size)
subfigs[1].suptitle('Weibull', fontsize=suptitle_size)
subfigs[2].suptitle('Lognormal', fontsize=suptitle_size)

ax = [None]*3
for row, subfig in enumerate(subfigs):
    ax[row] = subfig.subplots(ncols=2)

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
ax[0][1].plot(vrm_exp.keys(), vrm_exp.values(), 'r', label='VRM', markersize=marker_size)
ax[1][0].plot(x, y_wei, 'r', label='Weibull', markersize=marker_size)
ax[1][1].plot(vrm_wei.keys(), vrm_wei.values(), 'r', label='VRM', markersize=marker_size)
ax[2][0].plot(x, y_log, 'r', label='Lognormal', markersize=marker_size)
ax[2][0].set_xlabel('Tempo')
ax[2][1].plot(vrm_log.keys(), vrm_log.values(), 'r', label='VRM', markersize=marker_size)
ax[2][1].set_xlabel('Tempo')

for a in ax:
    a[0].set_ylim(0,1)
    a[0].set_ylabel('Densidade')
    a[1].set_ylabel('VMR')

plt.show()
