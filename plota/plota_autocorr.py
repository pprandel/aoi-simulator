from enum import auto
from matplotlib import colors
import matplotlib.pyplot as plt
import json
import numpy as np
from scipy.signal import correlate

def calc_int_autocor_time(Q):
        n = len(Q)
        mean = np.mean(Q)
        norm = (Q - mean)
        var_q = np.var(Q)
        result = correlate(norm, norm, mode='same')
        acorr = result [n//2 + 1:]  / (np.var(Q) * np.arange(n-1, n//2, -1))
        # acorr = result  / (var_q * np.arange(n+1,1,-1))
        auto_sum = 0
        M = len(acorr)
        print(M)
        for i in range(M):
                auto_sum = auto_sum + (1 - (i+1)/M)*acorr[i]
        auto_sum = 1 + 2*auto_sum
        # auto_sum = 1 + 2*acorr.sum()
        print("Integrated autocorrelation times: %f" %auto_sum)
        print("Variance of Q_mean: %f" %(np.var(Q)/len(Q)))
        true_var = np.var(Q)/(len(Q)/auto_sum)
        print("Variance corrected: %f" %true_var)
        return abs(auto_sum), acorr

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

ro = 0.9
mu = 1
aoi_analyt  = calc_analitic_aoi(ro,mu)

data_file = "resultados/A_vec.txt"
with open (data_file, 'r') as d:
        A = json.load(d)

data_file = "resultados/Q_vec.txt"
with open (data_file, 'r') as d:
        Q = json.load(d)

data_file = "resultados/V_vec.txt"
with open (data_file, 'r') as d:
        V = json.load(d)

V = [v**0.5 for v in V]

alfa, acorr = calc_int_autocor_time(Q)

V_corrigido = [(v * (alfa)**0.5) for v in V]
# var_delta = (100/250)**2 * var_Q
# RMSE = var_delta**0.5
print("RMSE: %f" %V_corrigido[-1])

fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
ln1 = ax1.plot(acorr, 'mediumblue', label='Estimated mean AoI')
# ln2 = ax2.plot(V, 'g', label='RMSE (without IAT)')
# ln3 = ax2.plot(V_corrigido, 'r', label='RMSE (with IAT)')

lns = ln1#+ln2+ln3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=18)

#ax1.axhline(y=aoi_analyt, color='indigo', linestyle='--')
ax1.text(10000, 9.8, r'Analytical $\Delta=10.21$', ha='left', va='center',fontsize=14, color='indigo')
# ax1.text(10000, 9.2, r'Estimated $\hat{\Delta}=6.07$', ha='left', va='center',fontsize=14, color='indigo')
ax1.text(10000, 9.4, 'Estimated RMSE = 0.2354', ha='left', va='center',fontsize=14, color='indigo')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.set_ylabel(r'$\hat{\Delta}$', fontsize=18)
# ax1.set_ylim(9,12)
# ax2.set_xlim(100,100000)
# ax2.set_ylabel('RMSE', fontsize=18)
# ax2.set_ylim(0,0.1)
#ax2.axhline(y=0.0001, color='r', linestyle='--')
#ax2.axvline(x=41910, color='r', linestyle='--')
#ax2.text(50000, 0.00013, r'Variance threshold = $10^{-4}$', ha='left', va='center',fontsize=14, color='r')
ax1.set_xlabel('N (number of packets)', fontsize=18)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
# ax2.tick_params(axis='y', labelsize=14)
# ax1.set_xticks(list(np.arange(0, 400001, 80000)))
fig.tight_layout()
plt.show()