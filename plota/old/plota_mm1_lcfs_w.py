import matplotlib.pyplot as plt
import ast

data_file = "resultados/analit_mm1_lcfs_w_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_mm1_lcfs_w_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

fig, ax = plt.subplots()
ax.plot(x_analit, y_analit, 'ro', label='Analytical')
ax.plot(x_sim, y_sim, 'b^', label="Simulated")
ax.set_xlabel(r'Server load $(\rho)$')
ax.set_ylabel('Mean AoI')
ax.set_title('Mean AoI for M/M/1 queue')
ax.legend()
plt.show()