import queueing_tool as qt
import numpy as np
import json, os, sys
import aoi_simulator as aoi

##### EXEMPLO 2: FILA SIMPLES COM DIVERSAS CARGAS #####

# REFERÊNCIA: @INPROCEEDINGS{Yates_often,
#             author={Kaul, Sanjit and Yates, Roy and Gruteser, Marco},
#             booktitle={2012 Proceedings IEEE INFOCOM},
#             title={Real-time status: How often should one update?},
#             year={2012},
#             pages={2731-2735},
#             doi={10.1109/INFCOM.2012.6195689}}

# Nome da simulação
sim_name = "exemplo_2"
# Cargas que serão usadas na simulação (1 simulação para cada carga)
RO = np.arange(0.1, 1, 0.1)
# Arredondamos as cargas para 1 casa decimal
RO = np.around(RO, decimals=1)
# Dicionário que retornará os resultados
aoi_dic = {}

# Iteramos sobre as cargas
for ro in RO:

    ### PARÂMETROS DA REDE ###
    # Criamos um grafo através de uma matriz de adjacências
    # Cada nó do grafo será uma fila na rede. O atributo 'edge_type' define os parâmetros da fila
    adjacency = {}
    adjacency[0] = {1: {'edge_type': 1}} # Nó 0 (será nossa fonte)
    adjacency[1] = {2: {'edge_type': 2}} # Nó 1 (será nosso monitor)
            
    # Instanciamos o grafo direcionado
    G = qt.QueueNetworkDiGraph(adjacency)

    # Definimos as classes das filas 
    q_cl = {1: aoi.AoIQueueServer, 2: aoi.AoIQueueServer}

    # Taxa de serviço do servidor
    mu = 1
    # Taxa de geração de pacotes
    lamb = mu * ro

    # Função geração de pacotes para o nó fonte (Poisson) 
    def f_gen_1(t): return t+ np.random.exponential(1/lamb)
    # Nossa fonte entrega os pacotes instantaneamente (não processa os pacotes)
    def f_ser_1(t): return t

    # Função de serviço para o nó monitor (Exponencial)
    def f_ser_2(t): return t + np.random.exponential(1/mu)

    # Configuração das filas (edge_type)
    q_ar = {
        1: {
            'arrival_f': f_gen_1,
            'service_f': f_ser_1,
            'num_servers': 1 
        },
        2: { 
            # Nó monitor não gera pacotes, apenas recebe do nó fonte
            'service_f': f_ser_2,
            # Quantidade de servidores
            'num_servers': 1 
        }
    }

    # Instanciamos a rede de filas a partir do grafo
    net = aoi.AoIQueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

    # Definimos para qual fila (ou nó) os dados serão coletados
    net.start_collecting_data(queues=1)

    # Inicializamos o nó fonte para que o mesmo gere pacotes
    net.initialize(queues=0)

    # Quantidade de eventos para a simulação (nr de pacotes * 3)
    net.simulate(n=300000)

    # Ao final da simulação coletamos os dados, indicando qual o nó monitor
    data = net.get_AoI_data(monitor=1)

    # Criamos uma pasta sim_data para armazenar os dados da simulação, caso ela não exista
    if not os.path.exists('sim_data'):
        os.makedirs('sim_data')

    # Salvamos os dados da simulação em um arquivo json, identificando-o pelo nome da simulação e a carga utilizada
    arq_nome = "sim_data/" + sim_name + "_ro_" + str(ro) + ".json"
    with open(arq_nome, 'w') as f:
        json.dump({str(k):v for k, v in data.items()}, f, indent=3)

    # Calculamos a AoI média e o erro da estimativa
    calc = aoi.MeanAoICalc(sim_name + "_ro_" + str(ro), arq_nome, 1)
    print(calc.aoi)
    aoi_dic[str(ro)] = calc.aoi[0]

# Criamos uma pasta resultados, caso ela não exista
if not os.path.exists('resultados'):
    os.makedirs('resultados')

# Salvamos os resultados da simulação na pasta, em um dicionário
arq_nome = "resultados/" + sim_name + ".json"
with open(arq_nome, 'w') as f:
    json.dump(aoi_dic, f, indent=3)