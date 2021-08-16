import matplotlib.pyplot as plt
import ast

data_file = "resultados/analit_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

fig, ax = plt.subplots(3, 1)

ax[0].plot(x_analit, y_analit, 'ro', label='Analítico')
ax[0].plot(x_sim, y_sim, 'b^', label="Simulado")
ax[0].set_xlabel(r'Carga no servidor $(\rho)$')
ax[0].set_ylabel('AoI médio')
ax[0].set_title('AoI médio para a fila M/M/1')
ax[0].legend()
ax[0].grid(True)

data_file = "resultados/analit_md1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_md1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

ax[1].plot(x_analit, y_analit, 'ro', label='Analítico')
ax[1].plot(x_sim, y_sim, 'b^', label="Simulado")
ax[1].set_xlabel(r'Carga no servidor $(\rho)$')
ax[1].set_ylabel('AoI médio')
ax[1].set_title('AoI médio para a fila M/D/1')
ax[1].legend()
ax[1].grid(True)

data_file = "resultados/analit_dm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_dm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

ax[2].plot(x_analit, y_analit, 'ro', label='Analítico')
ax[2].plot(x_sim, y_sim, 'b^', label="Simulado")
ax[2].set_xlabel(r'Carga no servidor $(\rho)$')
ax[2].set_ylabel('AoI médio')
ax[2].set_title('AoI médio para a fila D/M/1')
ax[2].legend()
ax[2].grid(True)

for ax in fig.get_axes():
    ax.label_outer()

fig.tight_layout()
plt.show()
