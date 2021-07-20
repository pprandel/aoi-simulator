from plota.compara_filas_analit import calc_dm1_aoi
import numpy as np
import matplotlib.pyplot as plt

def calc_multi_mm11_PS(ro, ro_i, mu):
    return (1/mu) * (1 + ro) * (1/ro_i)

RO = list(np.arange(0.1, 1, 0.1))
RO_1 = list(np.arange(0.5, 1, 0.5))
mu = 1

f1_aoi = {}
f2_aoi = {}