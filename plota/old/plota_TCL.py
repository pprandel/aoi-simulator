import matplotlib.pyplot as plt
import json

data_file = "resultados/TCL_prova.json"
with open (data_file, 'r') as d:
        data = json.load(d)

aoi = []
rmse = []
for d in data:
        aoi.append(d["MeanAoI"])
        rmse.append(d["RMSE"])

fig, ax = plt.subplots()
ax.hist(aoi, color='r', label='Analytical')
# ax.plot(rmse, 'b^', label="Simulated")
# ax.set_xlabel(r'Server load $(\rho)$')
# ax.set_ylabel('Mean AoI')
# ax.set_title('Mean AoI for D/M/1 queue')
# ax.legend()

plt.show()