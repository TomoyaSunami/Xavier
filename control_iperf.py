
import subprocess
import os

def start(pid_txt,ip="192.168.0.3",port="5002",bandwidth="10M"):
    par_pid = os.getpid()
    #print("par_pid: {}".format(par_pid))
    cmd = "iperf -u -t 20 -c " + ip + " -p " + port + " -b " + bandwidth
    #cmd = "iperf -s -u"
    proc = subprocess.Popen(cmd.split(" "))
    chi_pid = proc.pid
    #print("par_pid: {}, chi_pid: {}".format(par_pid,chi_pid))
    with open(pid_txt,'w') as f:
        f.write(str(chi_pid))
    
 

def kill(pid_txt):
    with open(pid_txt,'r') as f:
        pid = f.read()
    #print("target pid: {}".format(pid))
    cmd = "kill -9 " + pid
    proc = subprocess.Popen(cmd.split(" "))    


