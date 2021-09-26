import matplotlib.pyplot as plt
import ast

data_file = "resultados/analit_mm1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_mm1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

fig, ax = plt.subplots(3, 1)

ax[0].plot(x_analit, y_analit, 'ro', markersize=7, label='Analytical')
ax[0].plot(x_sim, y_sim, 'b^', markersize=7,label="Simulated")
ax[0].set_xlabel(r'Server load $(\rho)$',fontsize=14)
ax[0].set_ylabel('Mean AoI',fontsize=14)
ax[0].set_title('M/M/1/1*',fontsize=16)
ax[0].tick_params(axis='x', labelsize=14)
ax[0].tick_params(axis='y', labelsize=14)
ax[0].legend(fontsize=16)
ax[0].grid(True)

data_file = "resultados/analit_md1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_md1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

ax[1].plot(x_analit, y_analit, 'ro', markersize=7,label='Analytical')
ax[1].plot(x_sim, y_sim, 'b^', markersize=7, label="Simulated")
ax[1].set_xlabel(r'Server load $(\rho)$',fontsize=14)
ax[1].set_ylabel('Mean AoI',fontsize=14)
ax[1].set_title('M/D/1/1*',fontsize=16)
ax[1].tick_params(axis='x', labelsize=14)
ax[1].tick_params(axis='y', labelsize=14)
ax[1].legend(fontsize=16)
ax[1].grid(True)

data_file = "resultados/analit_dm1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_analit = data.keys()
y_analit = data.values()

data_file = "resultados/sim_dm1_lcfs_s_aoi.txt"
with open (data_file, 'r') as d:
        data = d.read()
        data = ast.literal_eval(data)

x_sim = data.keys()
y_sim = data.values()

ax[2].plot(x_analit, y_analit, 'ro',markersize=7, label='Analytical')
ax[2].plot(x_sim, y_sim, 'b^',markersize=7, label="Simulated")
ax[2].set_xlabel(r'Server load $(\rho)$', fontsize=14)
ax[2].set_ylabel('Mean AoI', fontsize=14)
ax[2].set_title('D/M/1/1*',fontsize=16)
ax[2].legend(fontsize=16)
ax[2].tick_params(axis='x', labelsize=14)
ax[2].tick_params(axis='y', labelsize=14)
ax[2].grid(True)

for ax in fig.get_axes():
    ax.label_outer()

fig.tight_layout()


plt.show()
