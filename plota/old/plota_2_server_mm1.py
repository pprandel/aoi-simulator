import matplotlib.pyplot as plt
import ast

data_file = "resultados/sim_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

data_file = "resultados/sim_2_servers_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim_2 = data.keys()
y_sim_2 = data.values()

data_file = "resultados/sim_4_servers_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim_4 = data.keys()
y_sim_4 = data.values()

data_file = "resultados/sim_8_servers_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim_8 = data.keys()
y_sim_8 = data.values()

data_file = "resultados/sim_16_servers_mm1_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim_16 = data.keys()
y_sim_16 = data.values()

fig, ax = plt.subplots()
ax.plot(x_sim, y_sim, 'mo', linestyle='--', label='1 server')
ax.plot(x_sim_2, y_sim_2, 'ys', linestyle='--', label='2 servers')
ax.plot(x_sim_4, y_sim_4, 'b^', linestyle='--', label='4 servers')
ax.plot(x_sim_8, y_sim_8, 'gv', linestyle='--', label='8 servers')
ax.plot(x_sim_16, y_sim_16, 'ro', linestyle='--', label='16 servers')
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.set_xlabel(r'Servers load $(\rho)$', fontsize=20)
ax.set_ylabel('Mean AoI', fontsize=20)
ax.set_ylim(1, 10)
ax.set_xticks([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
ax.legend(fontsize=14)
ax.grid(True)
plt.show()