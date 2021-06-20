import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt

def calc_mm1_PS(ro, mu):
    return (1/mu) * (1 + 1/ro)

def calc_dm1_PS(ro, mu):
    return (1/mu) * (1 + 1/(2*ro))

def calc_md1_PS(ro, mu):
     return (1/mu) * (np.exp(ro) / ro)

def calc_mm1_PW(ro, mu):
    return (1/mu) * (1 + 1/ro + ( (ro**2)*(1+3*ro+ro**2) ) / ( (1+ro+ro**2)*(1+ro)**2 ) )

def calc_dm1_PW(ro, mu):
    return (1/mu) * ( 1/(2*ro) + ( 1 / ( 1- ( (1/ro)*np.exp(-(1/ro)) ) ) ) )

def calc_md1_PW(ro, mu):
    return (1/mu) * ( ( ( 1/(1+ro*np.exp(ro)) ) * (1/2 + 1/ro) ) + ( (np.exp(ro) - (1+ro) ) / (ro*np.exp(ro)) ) + 3/2 )

RO = list(np.arange(0.1, 3, 0.01))
mu = 1

mm1_PS = {}
md1_PS = {}
dm1_PS = {}
mm1_PW = {}
md1_PW = {}
dm1_PW = {}

for ro in RO:
    mm1_PS[ro] = calc_mm1_PS(ro, mu)
    md1_PS[ro] = calc_md1_PS(ro, mu)
    dm1_PS[ro] = calc_dm1_PS(ro, mu)
    mm1_PW[ro] = calc_mm1_PW(ro, mu)
    md1_PW[ro] = calc_md1_PW(ro, mu)
    dm1_PW[ro] = calc_dm1_PW(ro, mu)

x = RO
fig, ax = plt.subplots()
ax.plot(x, mm1_PS.values(), 'r-', markersize=7, label='M/M/1/1*')
ax.plot(x, md1_PS.values(), 'b-', markersize=7, label="M/D/1/1*")
ax.plot(x, dm1_PS.values(), 'g-', markersize=7, label="D/M/1/1*")
ax.plot(x, mm1_PW.values(), 'y-', markersize=7, label='M/M/1/2*')
ax.plot(x, md1_PW.values(), 'k-', markersize=7, label="M/D/1/2*")
ax.plot(x, dm1_PW.values(), 'c-', markersize=7, label="D/M/1/2*")


ax.set_xlabel(r'Carga no servidor $\rho$', fontsize=16)
ax.set_ylabel('AoI média $\Delta$', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=16)
ax.set_xlim(0, 3)
ax.set_xticks(list(np.arange(0.2, 3, 0.4)))
ax.grid(True)
plt.show()