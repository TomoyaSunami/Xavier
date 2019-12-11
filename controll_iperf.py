
import os
import sys
import subprocess
from time import sleep
import concurrent.futures

"""
class IPERF:
    def __init__(self):
        self.port = 5001
        self.pid = 0
    def set_port(self,port):
        self.port = port
    def start_iperf(self):
        pid = os.getpid()
        print("start iperf pid: {}".format(pid))
        cmd = "iperf -c 192.168.0.3 -u -t 60" + " -p " + str(self.port)
        proc = subprocess.Popen(cmd.split(" "))
        chi_pid = proc.pid
        print("proc pid: {}".format(chi_pid))
        self.pid = chi_pid
    def kill_iperf(self):
        print("target pid: {}".format(self.pid))
        cmd = "kill " + str(self.pid)
        proc = subprocess.Popen(cmd.split(" "))
"""

def naive_start_iperf():
    port = 5002
    cmd = "iperf -c 192.168.0.3 -u -t 60" + " -p " + str(port)
    proc = subprocess.Popen(cmd.split(" "))
    chi_pid = proc.pid
    print("naive pid".format(chi_pid))
    path = "naive_iperf_pid.txt"
    with open(path, 'w') as f:
        f.write(str(chi_pid))

def hmm_start_iperf():
    port = 5003
    cmd = "iperf -c 192.168.0.3 -u -t 60" + " -p " + str(port)
    proc = subprocess.Popen(cmd.split(" "))
    chi_pid = proc.pid
    print("hmm pid".format(chi_pid))
    path = "hmm_iperf_pid.txt"
    with open(path, 'w') as f:
        f.write(str(chi_pid))

def avg_start_iperf():
    port = 5004
    cmd = "iperf -c 192.168.0.3 -u -t 60" + " -p " + str(port)
    proc = subprocess.Popen(cmd.split(" "))
    chi_pid = proc.pid
    print("avg pid".format(chi_pid))
    path = "avg_iperf_pid.txt"
    with open(path, 'w') as f:
        f.write(str(chi_pid))        

def kill_iperf(pid):
    cmd = "kill " + pid
    proc = subprocess.Popen(cmd.split(" "))

def main():
    print("controll_iperf.py is loaded")
    path = "iperf_flag.txt"
    

    if not os.path.isfile(path):        

        print("Error not exist the file")
        sys.exit(1)
    
    cores = os.cpu_count()
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=cores*5)
    sleep(5)
    print("-----start------")
    while(1):
        sleep(0.2)
        
        
        with open(path, mode='r') as f:
            str_r = [s.strip().split(",") for s in f.readlines()]
            str_w = str_r
        
        for i in range(1,4):
            if str_r[i][1]=="OFF" and str_r[i][2]=="True":
                if i == 1 :
                    executor.submit(naive_start_iperf)
                elif i == 2 :
                    executor.submit(hmm_start_iperf)
                else :
                    executor.submit(avg_start_iperf)
                str_w[i][1] = "ON"
                str_w[i][2] = "False"
            elif str_r[i][1]=="ON" and str_r[i][3]=="True":
                if i == 1 :
                    pid_path = "naive_iperf_pid.txt"
                elif i == 2 :
                    pid_path = "hmm_iperf_pid.txt"
                else :
                    pid_path = "avg_iperf_pid.txt"
                with open(pid_path, 'r') as f:
                    pid = f.read()
                kill_iperf(pid)
                str_w[i][1] = "OFF"
                str_w[i][3] = "False"
        
        with open(path, mode='w') as f:
            str_w = "\n".join([",".join(str_w[0][:]),",".join(str_w[1][:]),",".join(str_w[2][:]),",".join(str_w[3][:])])
            
            f.write(str_w)
        
    
if  __name__=="__main__":
    main()
