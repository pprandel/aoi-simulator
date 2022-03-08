import matplotlib.pyplot as plt
import json
import numpy as np

# Função que retorna valores analíticos para a fila M/M/1
def calc_analitic_mm1(ro, mu):
    return (1/mu) * (1 + 1/ro + (ro**2/(1-ro)) )

### Parâmetros da figura ###
fig, ax = plt.subplots()
marker_size = 10
ax_label_size = 12
label_size = 12
title_size = 14
legend_size = 12

# Cargas
ros = []
# Valores analíticos
mm1_analitico = []
# Valores simulados
mm1_sim = []
# Erro máximo
mm1_max_RMSE = 0
# Carregamos os resultados da simulação
data_file = "resultados/exemplo_2.json"
with open (data_file, 'r') as d:
        data = json.load(d)
for ro, value in data.items():
        ro = float(ro)
        ros.append(ro)
        # Valor analítico
        mm1_analitico.append(calc_analitic_mm1(ro,1))
        mm1_sim.append(value["MeanAoI"])
        RMSE = value["RMSE"]
        if RMSE > mm1_max_RMSE:
                mm1_max_RMSE = RMSE

ax.plot(ros, mm1_analitico, 'rv', label='Analítico', markersize=marker_size)
ax.plot(ros, mm1_sim, 'b^', label="Simulado", markersize=marker_size)
ax.set_xlabel(r'Carga no servidor $(\rho)$', fontsize=label_size)
ax.set_ylabel('AoI médio', fontsize=label_size)
ax.set_title('AoI médio para a fila M/M/1', fontsize=title_size)
text = "REQM < " + str(np.round(mm1_max_RMSE, decimals=2))
ax.text(0.5, 10, text, ha='center', va='top',fontsize=14, color='indigo', weight='bold')
ax.legend(fontsize=legend_size, loc='lower right')
ax.grid(True)

xlim = (0.05, 0.95)
ylim = (2, 12)
marker_size = 15
plt.setp(ax, xlim=xlim, ylim=ylim)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.set_yticks(list(np.arange(2, 12, 2)))
ax.label_outer()

fig.tight_layout()
plt.show()
