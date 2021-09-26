import matplotlib.pyplot as plt
import ast

data_file = "resultados/analit_multi_server_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_multi_server_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

data_file = "resultados/analit_multi_server_10sv.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

y_analit_10 = data.values()

data_file = "resultados/sim_multi_server_10sv.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

y_sim_10 = data.values()

fig, ax = plt.subplots()
ax.plot(x_analit, y_analit, 'ro', label='Analítico')
ax.plot(x_analit, y_analit_10, 'yo', label='Analítico 10')
ax.plot(x_sim, y_sim, 'b^', label="Simulado")
ax.plot(x_sim, y_sim_10, 'go', label='Simulado 10')
ax.set_xlabel(r'Carga no servidor $(\rho)$')
ax.set_ylabel('AoI médio')
ax.set_title('AoI médio para a fila M/M/1')
ax.legend()
plt.show()