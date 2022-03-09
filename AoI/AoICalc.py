import json
import numpy as np
from scipy.signal import correlate

"""
Base class that calculates Age of Information (AoI)

"""

class AoICalc():
    
    def __init__(self, sim_id, data_file, num_sources, save_AoI_seq="None", save_Q_seq="None", **kwargs):

        self.sim_id = sim_id
        self.data_file = data_file
        self.num_sources = num_sources
        self.save_AoI_seq = save_AoI_seq
        self.save_Q_seq = save_Q_seq
        
        self.aoi = {}

        for i in range(self.num_sources):
            self.aoi[i] = {}
            self.aoi[i]["Preempted"] = 0
            self.aoi[i]["Obsolete"] = 0
            self.aoi[i]["RMSE"] = 0

        # Load data
        with open (self.data_file, 'r') as d:
            data = json.load(d)

        # Split sources
        self.splitted_data = {}
        preempted = 0
        obsolete = 0
        for id, value in data.items():
            id_splitted = id.split(",")
            source = int(id_splitted[0][1:])
            gen_time = float(id_splitted[2][0:-1])
            deliv_time = value[2]
            times = (gen_time, deliv_time)
            if source in self.splitted_data:
                # Remove preempted
                if deliv_time == 0:
                    preempted = preempted + 1
                    continue
                # Remove obsolete
                elif gen_time < self.splitted_data[source][-1][0]:
                    obsolete = obsolete +1
                    continue
                self.splitted_data[source].append(times)
            else:
                self.splitted_data[source] = []
                self.splitted_data[source].append(times)
            self.aoi[i]["Preempted"] = preempted
            self.aoi[i]["Obsolete"] = obsolete

    def save_seqences(self, i):
        if self.save_AoI_seq != "None":
            try:
                arq_name = self.save_AoI_seq + "/" + self.sim_id + "_source_" + str(i) + ".txt"
                with open(arq_name, 'w') as f:
                    f.write(str(self.Q_vector))
            except Exception as e:
                print("Error saving AoI sequence: %s" %e)

        if self.save_Q_seq != "None":
            try:
                arq_name = self.save_Q_seq + "/" + self.sim_id + "_source_" + str(i) + ".txt"
                with open(arq_name, 'w') as f:
                    f.write(str(self.Q_vector))
            except Exception as e:
                print("Error saving Q sequence: %s" %e)

"""
Class that calculates Mean Age of Information (Mean AoI)

Parameters
----------
sim_id: str
    identification of simulation
data_file : json file
    json with class:Agent "agent_id" as keys and list [arrival, service
    start, departure times, agents waiting to be served and the total agents in the
    system] as values
num_sources: int
    number of sources of Agents. Mean AoI will be calculated for each source - Integer
save_AoI_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI
    example: "/tmp/my_sim"
save_Q_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI areas Q
    example: "/tmp/my_sim"

Returns
----------
mean_aoi: dict
    dict with sources as keys and {"MeanAoI", "RMSE", "Preempted", "Obsolete"} as values
"""
class MeanAoICalc(AoICalc):

    def __init__(self, sim_id, data_file, num_sources, save_AoI_seq="None", save_Q_seq="None", **kwargs):
        super().__init__(sim_id, data_file, num_sources, save_AoI_seq, save_Q_seq, **kwargs)

        self.aoi_vector = []
        self.Q_vector = []
        for i in range(self.num_sources):
            self.aoi[i]["MeanAoI"] = np.inf

        print("Calculating Mean AoI values for simulation [%s]" %self.sim_id)

        for i in self.splitted_data.keys():
            try:
                self.calc_aoi(i)
            except Exception as e:
                print("Error calculating AoI for source %d: %s" %(i, e))
            try:
                self.save_seqences(i)
            except Exception as e:
                print("Error saving sequences for source %d: %s" %(i, e))

        # Calculates mean AoI for a data array  
    def calc_aoi(self, source):
        
        self.aoi_vector.clear()
        self.Q_vector.clear()
        
        def Qi(Ti, Yi):
            Q = Ti*Yi + 0.5*(Yi**2)
            return Q
        
        data = self.splitted_data[source]
        ti = data[0][0] # Gen time packet #0
        t_start = ti
        ti_linha = 0
        Ti = 0
        Qi_total = 0
        N = 0 # Total delivered packets
        data.pop(0) # Remove first entry
        for value in data:
            if value[1] == 0:
                continue
            N = N + 1
            if value[0] < ti:
                print("Error: obsolete packet!")
                print("gen_time = %f" %value[0])
                break
            Yi = value[0] - ti
            ti = value[0]
            ti_linha = value[1]
            Ti = ti_linha - ti
            Qi_now = Qi(Ti, Yi)
            Qi_total = Qi_total + Qi_now
            mean_aoi = Qi_total/(ti_linha-t_start)
            self.aoi_vector.append(mean_aoi)
            self.Q_vector.append(Qi_now)
        Qi_total = Qi_total + 0.5*(Ti**2)
        self.aoi[source]["MeanAoI"] = Qi_total / (ti_linha - t_start)
        self.aoi[source]["RMSE"] = self.calc_RMSE(N, ti_linha)

    # Caclulate root mean squared error
    def calc_RMSE(self, N, tau):
        Q = self.Q_vector
        mean_q = np.mean(Q)
        var_q = np.var(Q)
        # Normalized Q
        norm_Q = (Q - mean_q)
        # Autocorrelation
        result = correlate(norm_Q, norm_Q, mode='same')
        acorr = result [N//2 + 1:]  / (var_q * np.arange(N-1, N//2, -1))
        M = len(acorr)
        iat = 0
        # IAT - Integrated autocorrelation times
        for i in range(M):
            iat = iat + (1 - (i+1)/M)*acorr[i]
        iat = 1 + 2*iat
        var_Q_mean = var_q/len(Q)
        true_var_Q_mean = var_Q_mean * iat
        var_aoi_mean = (N/tau)**2 * true_var_Q_mean
        RMSE = var_aoi_mean**0.5
        return RMSE

"""
Class that calculates Mean Peak Age of Information (Mean pAoI)

Parameters
----------
sim_id: str
    identification of simulation
data_file : json file
    json with class:Agent "agent_id" as keys and list [arrival, service
    start, departure times, agents waiting to be served and the total agents in the
    system] as values
num_sources: int
    number of sources of Agents. Mean AoI will be calculated for each source - Integer
save_AoI_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI
    example: "/tmp/my_sim"
save_Q_seq: str (optional, defalut: "None")
    path to folder where to save the sequence of calculated AoI areas Q
    example: "/tmp/my_sim"

Returns
----------
mean_peak_aoi: dict
    dict with sources as keys and {"MeanPeakAoI", "RMSE", "Preempted", "Obsolete"} as values
"""
class MeanPeakAoICalc(AoICalc):

    def __init__(self, sim_id, data_file, num_sources, save_AoI_seq="None", save_Q_seq="None", **kwargs):
        super().__init__(sim_id, data_file, num_sources, save_AoI_seq, save_Q_seq, **kwargs)

        self.paoi_vector = []
        for i in range(self.num_sources):
            self.aoi[i]["MeanPeakAoI"] = np.inf

        print("Calculating Mean Peak AoI values for simulation [%s]" %self.sim_id)
                
        for i in self.splitted_data.keys():
            try:
                self.calc_aoi(i)
            except Exception as e:
                print("Error calculating AoI for source %d: %s" %(i, e))
            try:
                self.save_seqences(i)
            except Exception as e:
                print("Error saving sequences for source %d: %s" %(i, e))

    def calc_aoi(self, source):
        self.paoi_vector.clear()
        
        # peak age calculation
        def Ai(Ti, Yi):
            return Ti + Yi

        data = self.splitted_data[source]
        ti = data[0][0] # Gen time packet #0
        N = 0 # total delivered packets
        data.pop(0) # Remove first entry
        for value in data:
            if value[1] == 0: 
                continue
            N = N + 1 
            if value[0] < ti:
                print("Error: obsolete packet!")
                print("gen_time = %f" %value[0])
                break
            Yi = value[0] - ti
            ti = value[0]
            ti_linha = value[1]
            Ti = ti_linha - ti
            self.paoi_vector.append(Ai(Ti, Yi))
        self.aoi[source]["MeanPeakAoI"] = np.mean(self.paoi_vector)
        self.aoi[source]["RMSE"] = self.calc_RMSE(N, source)

    def calc_RMSE(self, N, source):
        # Variance
        var_A = np.var(self.paoi_vector)
        # Normalized A
        norm_A = (self.paoi_vector - self.aoi[source]["MeanPeakAoI"])
        # Autocorrelation
        result = correlate(norm_A, norm_A, mode='same')
        acorr = result [N//2 + 1:]  / (var_A * np.arange(N-1, N//2, -1))
        M = len(acorr)
        iat = 0
        # IAT
        for i in range(M):
            iat = iat + (1 - (i+1)/M)*acorr[i]
        iat = 1 + 2*iat
        var_A_mean = var_A/N
        true_var_A_mean = var_A_mean * iat
        RMSE = true_var_A_mean**0.5
        return RMSE