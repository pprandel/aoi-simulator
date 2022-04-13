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

fig, ax = plt.subplots()
ax.plot(x_analit, y_analit, 'ro', label='Analítico')
ax.plot(x_sim, y_sim, 'b^', label="Simulado")
ax.set_xlabel(r'Carga no servidor $(\rho)$')
ax.set_ylabel('AoI médio')
ax.set_title('AoI médio para a fila M/M/1')
ax.legend()
plt.show()