from matplotlib import colors
import matplotlib.pyplot as plt
import ast
import numpy as np
from scipy.special import lambertw

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

ro = 0.5
mu = 1
aoi_analyt  = calc_analitic_aoi(ro,mu)

data_file = "resultados/Q_vec.txt"
with open (data_file, 'r') as d:
        Q = d.read()
        Q = ast.literal_eval(Q)
data_file = "resultados/V_vec.txt"
with open (data_file, 'r') as d:
        V = d.read()
        V = ast.literal_eval(V)
V = [v**(0.5) for v in V]

n = len(Q)
print(n)
mean = np.mean(Q)
norm = (Q - mean)
result = np.correlate(norm, norm, mode='same')
print(len(result))
acorr = result[n//2 + 1:] / (np.var(Q) * np.arange(n-1, n//2, -1))
auto_sum = acorr.sum()
# lag = np.abs(acorr).argmax() + 1
# r = acorr[lag-1]   
print(auto_sum)
print(np.var(Q)/len(Q))
true_var = np.var(Q)/(len(Q)/auto_sum)
print(true_var)

fig, ax1 = plt.subplots()
ln1 = ax1.plot(Q, 'mediumblue', label='Mean AoI')
ax2 = ax1.twinx()
ln2 = ax2.plot(V, 'g', label='RMSE')

lns = ln1+ln2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=18)

ax1.axhline(y=aoi_analyt, color='indigo', linestyle='--')
ax1.text(10500, 3.4, r'Analytical value ($\Delta=3.5$)', ha='left', va='center',fontsize=14, color='indigo')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.set_ylabel(r'$\hat{\Delta}$', fontsize=18)
# ax1.set_ylim(2.5,4.5)
# ax2.set_xlim(-100,20000)
# ax2.set_ylabel('RMSE', fontsize=18)
# ax2.set_ylim(0.03,0.1)
#ax2.axhline(y=0.0001, color='r', linestyle='--')
#ax2.axvline(x=41910, color='r', linestyle='--')
#ax2.text(50000, 0.00013, r'Variance threshold = $10^{-4}$', ha='left', va='center',fontsize=14, color='r')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)
fig.tight_layout()
#plt.show()