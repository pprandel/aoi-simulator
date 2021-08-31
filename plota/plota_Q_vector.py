from matplotlib import colors
import matplotlib.pyplot as plt
import ast
import numpy as np
from scipy.special import lambertw

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

ro = 0.5
aoi_analyt  = calc_analitic_aoi(ro,1)

data_file = "resultados/Q_vec.txt"
with open (data_file, 'r') as d:
        Q = d.read()
        Q = ast.literal_eval(Q)

data_file = "resultados/V_vec.txt"
with open (data_file, 'r') as d:
        V = d.read()
        V = ast.literal_eval(V)

fig, ax1 = plt.subplots()
ln1 = ax1.plot(Q, 'mediumblue', label='Mean AoI')
ax2 = ax1.twinx()
ln2 = ax2.plot(V, 'g', label='Mean squared error')

lns = ln1+ln2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=18)

ax1.axhline(y=aoi_analyt, color='indigo', linestyle='--')
ax1.text(2000, 3.25, r'Analytical value ($\gamma=3.5$)', ha='left', va='center',fontsize=14, color='indigo')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.set_ylabel(r'$\hat{\gamma}$', fontsize=18)
ax2.set_xlim(-1000,25000)
ax2.set_ylabel(r'$E((\hat{\gamma}-\gamma)^2)$', fontsize=18)
ax2.set_ylim(0,0.0005)
#ax2.axhline(y=0.0001, color='r', linestyle='--')
#ax2.axvline(x=41910, color='r', linestyle='--')
#ax2.text(50000, 0.00013, r'Variance threshold = $10^{-4}$', ha='left', va='center',fontsize=14, color='r')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)
fig.tight_layout()
plt.show()