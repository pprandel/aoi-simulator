from matplotlib import colors
import matplotlib.pyplot as plt
import ast
import numpy as np
from scipy.special import lambertw

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

ro = 0.5
aoi_analyt  = 4.69
data_file = "resultados/Q_vec_0.txt"
with open (data_file, 'r') as d:
        Q0 = d.read()
        Q0 = ast.literal_eval(Q0)

data_file = "resultados/Q_vec_1.txt"
with open (data_file, 'r') as d:
        Q1 = d.read()
        Q1 = ast.literal_eval(Q1)

fig, ax1 = plt.subplots()

print(np.mean(Q0))
print(np.var(Q0))
print(np.mean(Q1))
print(np.var(Q1))
ax1.hist(Q0, color='mediumblue', label='Q0', bins='auto')
ax1.hist(Q1, color='orange', label='Q1', bins='auto')



# ln1 = ax1.plot(Q, 'mediumblue', label='Mean AoI')
# ax2 = ax1.twinx()
# ln2 = ax2.plot(V, 'g', label='Mean squared error')

# lns = ln1+ln2
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0, fontsize=18)

# ax1.axhline(y=aoi_analyt, color='indigo', linestyle='--')
# ax1.text(2000, 3.25, r'Analytical value ($\gamma=3.5$)', ha='left', va='center',fontsize=14, color='indigo')
# ax1.set_xlabel('N (number of packets)', fontsize=18)
# ax1.set_ylabel(r'$\hat{\gamma}$', fontsize=18)
# ax2.set_xlim(-1000,100000)
# ax2.set_ylabel(r'$E((\hat{\gamma}-\gamma)^2)$', fontsize=18)
# ax2.set_ylim(0,0.01)
# #ax2.axhline(y=0.0001, color='r', linestyle='--')
# #ax2.axvline(x=41910, color='r', linestyle='--')
# #ax2.text(50000, 0.00013, r'Variance threshold = $10^{-4}$', ha='left', va='center',fontsize=14, color='r')
# ax1.set_xlabel('N (number of packets)', fontsize=18)
# ax1.tick_params(axis='x', labelsize=14)
# ax1.tick_params(axis='y', labelsize=14)
# ax2.tick_params(axis='y', labelsize=14)
# fig.tight_layout()
plt.show()