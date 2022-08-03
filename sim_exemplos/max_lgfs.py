import queueing_tool as qt
import numpy as np
import json, os
import aoi_simulator as aoi

print(aoi)

dist_param = {
    'exp': {
        'mean_sv': 1,
        'f_ser': lambda: np.random.exponential(1),
        'mrl_file': "data_aux_dev/MRL_exp_1.json"
    },
    'weib': {
        'mean_sv': 0.886,
        'f_ser': lambda: np.random.weibull(2),
        'mrl_file': "data_aux_dev/MRL_weib_2.json"
    },
    'logn': {
        'mean_sv': 1.384,
        'f_ser': lambda: np.random.lognormal(0.2,0.5),
        'mrl_file': "data_aux_dev/MRL_ln_02_05.json"
    }
}

dist = 'weib'

simulations = {"2": "masif_lgfs_" + dist}


for code, sim in simulations.items():

    # Nome da simulação
    sim_name = sim
    # Cargas que serão usadas na simulação (1 simulação para cada carga)
    RO = np.arange(0.2, 3, 0.2)
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
        N = 50
        C = 3
        for i in range(N):
            adjacency[i] = {N: {'edge_type': 1}}
        adjacency[N] = {N+1: {'edge_type': 2}}
                
        # Instanciamos o grafo direcionado
        G = qt.QueueNetworkDiGraph(adjacency)

        # Definimos as classes das filas 
        q_cl = {1: aoi.AoIQueueServer, 2: aoi.LgfsMultiServerNoPreemption}

        # Taxa de serviço do servidor
        mu = 1 / dist_param[dist]['mean_sv']
        # Taxa de geração de pacotes
        lamb = (ro * mu * C) / N

        # Função geração de pacotes para o nó fonte (Poisson) 
        def f_gen_1(t): return t+ np.random.exponential(1/lamb)
        # Atraso da rede
        def f_ser_1(t): return t + np.random.exponential(0.5)

        # Função de serviço para o nó monitor
        def f_ser_2(t): return t + dist_param[dist]['f_ser']()
        # Configuração das filas (edge_type)
        q_ar = {
            1: {
                'arrival_f': f_gen_1,
                'service_f': f_ser_1,
                'num_servers': np.infty
            },
            2: { 
                'service_f': f_ser_2,
                #'service_mean': dist_param[dist]['mean_sv'],
                'num_servers': C,
                'preemption': int(code),
                #'mrl_file': dist_param[dist]['mrl_file']
            }
        }

        # Instanciamos a rede de filas a partir do grafo
        net = aoi.AoIQueueNetwork(g=G, q_classes=q_cl, q_args=q_ar, max_agents=np.infty)

        # Definimos para qual fila (ou nó) os dados serão coletados
        net.start_collecting_data(queues=N)

        # Inicializamos o nó fonte para que o mesmo gere pacotes
        net.initialize(queues=range(N))

        # Quantidade de eventos para a simulação (nr de pacotes * 3)
        net.simulate(n=200000)

        # Ao final da simulação coletamos os dados, indicando qual o nó monitor
        data = net.get_AoI_data(monitor=N)

        # Criamos uma pasta sim_data para armazenar os dados da simulação, caso ela não exista
        if not os.path.exists('sim_data'):
            os.makedirs('sim_data')

        # Salvamos os dados da simulação em um arquivo json, identificando-o pelo nome da simulação e a carga utilizada
        arq_nome = "sim_data/" + sim_name + "_ro_" + str(ro) + ".json"
        with open(arq_nome, 'w') as f:
            json.dump({str(k):v for k, v in data.items()}, f, indent=3)

        # Calculamos a AoI média e o erro da estimativa
        calc = aoi.MeanAoICalc(sim_name + "_ro_" + str(ro), arq_nome, N)
        print(calc.aoi)
        aoi_vector = []
        for source in calc.aoi.values():
            aoi_vector.append(source["MeanAoI"])
        print("Mean AoI for all sources:")
        mean_aoi = np.mean(aoi_vector)
        print(mean_aoi)
        aoi_dic[str(ro)] = mean_aoi
    # Criamos uma pasta resultados, caso ela não exista
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    # Salvamos os resultados da simulação na pasta, em um dicionário
    arq_nome = "resultados/" + sim_name + ".json"
    with open(arq_nome, 'w') as f:
        json.dump(aoi_dic, f, indent=3)