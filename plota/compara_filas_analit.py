import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt

def calc_mm1_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

def beta(ro):
    return -ro * lambertw( -1/ro * np.exp(-1/ro) )

def calc_dm1_aoi(ro, mu):
    return (1/mu) * (1/(2*ro) + 1/(1-beta(ro)) )

def calc_md1_aoi(ro, mu):
    return (1/mu) * ( 1/(2*(1-ro)) + 0.5 + ( (1-ro)*np.exp(ro) ) / ro ) 

RO = list(np.arange(0.1, 0.91, 0.04))
mu = 1

mm1_aoi = {}
md1_aoi = {}
dm1_aoi = {}

for ro in RO:
    mm1_aoi[ro] = calc_mm1_aoi(ro, mu)
    md1_aoi[ro] = calc_md1_aoi(ro, mu)
    dm1_aoi[ro] = calc_dm1_aoi(ro, mu)

x = RO
fig, ax = plt.subplots()
ax.plot(x, mm1_aoi.values(), 'ro', markersize=7, label='M/M/1')
ax.plot(x, md1_aoi.values(), 'b^', markersize=7, label="M/D/1")
ax.plot(x, dm1_aoi.values(), 'gv', markersize=7, label="D/M/1")
ax.set_xlabel(r'Carga no servidor $\rho$', fontsize=16)
ax.set_ylabel('AoI média $\Delta$', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=16, loc='upper center')
ax.set_xlim(0, 1)
ax.set_xticks(list(np.arange(0.1, 1, 0.1)))
ax.grid(True)
plt.show()