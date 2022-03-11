import queueing_tool as qt
import numpy as np
import json, os
import aoi_simulator as aoi

##### EXEMPLO 2: FILA SIMPLES COM DUAS FONTES #####

# Nome da simulação
sim_name = "exemplo_3"
# Cargas totais no servidor (ro1 + ro2) que serão usadas na simulação
RO = np.arange(0.1, 1, 0.1)
# Arredondamos as cargas para 1 casa decimal
RO = np.around(RO, decimals=1)
# Dicionário que retornará os resultados
aoi_dic = {}

# Iteramos sobre as cargas totais
for ro in RO:
    # Para cada carga total no servidor faremos diversas combinações das cargas individuais de cada fonte
    print("Simulando para a carga ro = %f" %ro)
    aoi_dic[str(ro)] = {}
    for percent in np.arange(0, 1.1, 0.1):
        ro_1 = round(ro*percent, 2)
        ro_2 = round(ro - ro_1, 2)
        print("ro_1: %f ro_2: %f " %(ro_1, ro_2))
        if ro_1 ==0:
            arr_1 = 0
        else:
            arr_1 = 1/ro_1
        if ro_2 ==0:
            arr_2 = 0
        else:
            arr_2 = 1/ro_2

        ### PARÂMETROS DA REDE ###
        # Criamos um grafo através de uma matriz de adjacências
        # Cada nó do grafo será uma fila na rede. O atributo 'edge_type' define os parâmetros da fila
        adjacency = {
                0: {2: {'edge_type': 1}}, # Nó 0: Fonte 1
                1: {2: {'edge_type': 2}}, # Nó 1: Fonte 2
                2: {3: {'edge_type': 3}}  # Nó 2: Monitor
        }
                
        # Instanciamos o grafo direcionado
        G = qt.QueueNetworkDiGraph(adjacency)

        # Definimos as classes das filas 
        q_cl = {1: aoi.AoIQueueServer, 2: aoi.AoIQueueServer, 3: aoi.AoIQueueServer}

        # Função geração de pacotes para os nós fonte (Poisson) - Taxa de geração de acordo com a carga de cada fonte
        def f_arr_1(t): return t+ np.random.exponential(arr_1)
        def f_arr_2(t): return t+ np.random.exponential(arr_2)
        # Nossas fontes entregam os pacotes instantaneamente (não processam os pacotes)
        def f_ser_1(t): return t

        # Função de serviço para o nó monitor - Fixa (Exponencial com média 1)
        def f_ser_2(t): return t + np.random.exponential(1)
        q_ar = {
            1: {
                'arrival_f': f_arr_1,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            2: {
                'arrival_f': f_arr_2,
                'service_f': f_ser_1,
                'num_servers': 1
            },
            3: {
                'service_f': f_ser_2,
                'num_servers': 1
            }
        }

        # Instanciamos a rede de filas a partir do grafo
        net = aoi.AoIQueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

        # Definimos para qual fila (ou nó) os dados serão coletados
        net.start_collecting_data(queues=2)

        # Inicializamos o nó fonte para que o mesmo gere pacotes
        if arr_1 == 0:
            net.initialize(queues=[1])
        elif arr_2 == 0:
            net.initialize(queues=[0])
        else:
            net.initialize(queues=[0,1])

        # Quantidade de eventos para a simulação (nr de pacotes * 3)
        net.simulate(n=3000)

        # Ao final da simulação coletamos os dados, indicando qual o nó monitor
        data = net.get_AoI_data(monitor=2)

        # Criamos uma pasta sim_data para armazenar os dados da simulação, caso ela não exista
        if not os.path.exists('sim_data'):
            os.makedirs('sim_data')

        # Salvamos os dados da simulação em um arquivo json, identificando-o pelo nome da simulação e a carga utilizada
        arq_nome = "sim_data/" + sim_name + "_ro_" + str(ro) + ".json"
        with open(arq_nome, 'w') as f:
            json.dump({str(k):v for k, v in data.items()}, f, indent=3)

        # Calculamos a AoI média e o erro da estimativa
        calc = aoi.MeanAoICalc(sim_name + "_ro_" + str(ro), arq_nome, 2)
        print(calc.aoi)
        aoi_dic[str(ro)][str(ro_1) + '_' + str(ro_2)] = calc.aoi

# Criamos uma pasta resultados, caso ela não exista
if not os.path.exists('resultados'):
    os.makedirs('resultados')

# Salvamos os resultados da simulação na pasta, em um dicionário
arq_nome = "resultados/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump(aoi_dic, f, indent=3)