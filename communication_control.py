import time
import numpy as np
import joblib
import subprocess

class IPERF:
    def __init__(self,ip):
        self.ip = ip
        self.port = ""
        self.bandwidth = ""
        self.pid = None
        self.state = "OFF"
        self.proc = None
    def set_port(self,port):
        self.port = " -p " + str(port)
    def set_bandwidth(self,bandwidth):
        self.bandwidth = " -b " + bandwidth
    def start(self):
        if self.state == "OFF":
            cmd = "iperf -u -t 60 -c " + self.ip + self.port + self.bandwidth
            proc = subprocess.Popen(cmd.split(" "))
            chi_pid = proc.pid
            print("proc pid: {}".format(chi_pid))
            self.pid = chi_pid
            self.state = "ON"
            self.proc = proc
    def kill(self):
        if self.state == "ON":
            #print("target pid: {}".format(self.pid))
            #cmd = "kill -9 " + str(self.pid)
            #proc = subprocess.Popen(cmd.split(" "))
            self.proc.kill()
            self.state = "OFF"
            

def load(path):
    x = ''
    while x == '':
        with open(path, 'r') as f:
            x = f.read()
    return int(x)

def stock(x_array, x, window_size):
    length = len(x_array)   
    if length < window_size:
        x_array = np.append(x_array,x)
    else :
        x_array = np.roll(x_array, -1)
        x_array[-1] = x  
    return x_array

def hmm_estimate(model, observed_sequence, pre_estimation):
    if len(observed_sequence) <= 1:
        return 0
    observed_sequence = np.array([observed_sequence]).T

    logprob,state_sequence = model.decode(observed_sequence)
    
    if model.emissionprob_[0,0] > model.emissionprob_[0,1] and model.emissionprob_[1,0] < model.emissionprob_[1,1]:
        estimation = 0 if state_sequence[-1] == 0 else 1
    elif model.emissionprob_[0,0] < model.emissionprob_[0,1] and model.emissionprob_[1,0] > model.emissionprob_[1,1]:
        estimation = 1 if state_sequence[-1] == 0 else 0
    else:
        estimation = pre_estimation

    return estimation

def mode_estimate(x_array):
    return int(sum(x_array)/len(x_array) + 0.5)

def save_sequence(x, hmm_estimation, mode_estimation):
    with open("observed_sequence.txt", mode='a') as f:
        str_w = str(x) + "\n"
        f.write(str_w)
    with open("decoded_state_sequence.txt", mode='a') as f:
        str_w = str(hmm_estimation) + "\n"
        f.write(str_w)
    with open("mode_observed_sequence.txt", mode='a') as f:
        str_w = str(mode_estimation) + "\n"
        f.write(str_w)

def main():
    x_array1 = np.empty([1,0],int)
    x_array2 = np.empty([1,0])

    model = joblib.load("HMM_1215.pkl")
    hmm_estimation = 0
    """
    #iperf1_base = IPERF("192.168.0.3")
    #iperf1_base.set_port(5002)
    #iperf1_base.set_bandwidth("1")
    iperf1 = IPERF("192.168.0.3")
    iperf1.set_port(5002)
    iperf1.set_bandwidth("10M")

    #iperf2_base = IPERF("192.168.0.3")
    #iperf2_base.set_port(5003)
    #iperf2_base.set_bandwidth("1")
    iperf2 = IPERF("192.168.0.3")
    iperf2.set_port(5003)
    iperf2.set_bandwidth("10M")
    """
    iperf3_base = IPERF("192.168.0.3")
    iperf3_base.set_port(5004)
    iperf3_base.set_bandwidth("1")
    iperf3 = IPERF("192.168.0.3")
    iperf3.set_port(5004)
    iperf3.set_bandwidth("10M")
    
    #iperf1_base.start()
    #iperf2_base.start()
    iperf3_base.start()
    
    time.sleep(1)
    print("-------\n\n\nrunning\n\n\n------")
    key = ""
    while key!=113:
        x = load("is_there_person.txt")
        x_array1 = stock(x_array1, x, 10)
        x_array2 = stock(x_array2, x, 10)

        hmm_estimation = hmm_estimate(model, x_array1, hmm_estimation)
        mode_estimation = mode_estimate(x_array2)
        """
        if x == 1:
            iperf1.start()
        else :
            iperf1.kill()
        """
        """"
        if hmm_estimation == 1:
            iperf2.start()
        else :
            iperf2.kill()
        """
        
        if mode_estimation == 1:
            iperf3.start()
        else :
            iperf3.kill()
        
        #save_sequence(x, hmm_estimation, mode_estimation)
        with open("is_there_person.txt",'w') as f:
            f.write("")
        key = cv2.waitKey(5)
    
    iperf3_base.kill()
    iperf3.kill()    

if  __name__=="__main__":
    main()
