from matplotlib import colors
import matplotlib.pyplot as plt
import ast
import numpy as np
from scipy.special import lambertw

def calc_analitic_aoi(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

ro = 0.9
aoi_analyt  = calc_analitic_aoi(ro,1)

data_file = "resultados/Q_vec.txt"
with open (data_file, 'r') as d:
        Q = d.read()
        Q = ast.literal_eval(Q)
# data_file = "resultados/V_vec.txt"
# with open (data_file, 'r') as d:
#         V = d.read()
#         V = ast.literal_eval(V)
# V = [v**(0.5) for v in V]

print(np.var(Q))
print(np.mean(Q))
fig, ax1 = plt.subplots()