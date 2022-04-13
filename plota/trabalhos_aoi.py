import matplotlib.pyplot as plt
import numpy as np 

ano = [
    2021,
    2020,
    2019,
    2018,
    2017,
    2016,
    2015,
    2014,
    2013,
    2012
]

qtd = [
    422,
    281,
    211,
    95,
    51,
    29,
    23,
    17,
    16,
    17
]

fig, ax = plt.subplots()
ax.plot(ano, qtd, '-ob', linewidth=2, markersize=7, label="Publicações relacionadas \n à AoI por ano")
ax.set_ylabel('Quantidade de publicações', fontsize=14)
ax.set_xlabel('Ano', fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.set_xticks(list(np.arange(2012, 2022, 1)))
ax.legend(fontsize=14, loc='upper center')
ax.set_ylim(0, 450)
ax.grid(True)
plt.show()