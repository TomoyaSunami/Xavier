
import os
import sys
import subprocess
from time import sleep
import concurrent.futures

def start_iperf():
    #cmd = "iperf -s -u -i 1"
    cmd = "iperf -c 192.168.0.3 -u -t 60"
    subprocess.call(cmd.split(" "))

def kill_iperf():
    cmd = "pkill -f iperf"
    subprocess.call(cmd.split(" "))  

def main():
    print("controll")
    path = "iperf_flag.txt"
    

    if not os.path.isfile(path):        

        print("Error not exist the file")
        sys.exit(1)
    
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    count = 1
    while(1):
        #print(count)

        with open(path, mode='r') as f:
            str_r = [s.strip().split(",") for s in f.readlines()]
            #print(str_r)
            discription = str_r[0][:]
            iperf_state = str_r[1][1]
            iperf_start = str_r[1][2]
            iperf_kill = str_r[1][3]
    
            if iperf_state=="OFF" and iperf_start=="True":
                str_w = str_r
                str_w = str_r               
                with open(path, mode='w') as f:
                    str_w[1][1] = "ON"
                    str_w[1][2] = "False"
                    str_w = "\n".join([",".join(str_w[0][:]),",".join(str_w[1][:])])
                    #print(str_w)
                    f.write(str_w)
                executor.submit(start_iperf)
                
                print("start iperf")

            elif iperf_state=="ON" and iperf_kill=="True":
                str_w = str_r
                with open(path, mode='w') as f:
                    str_w[1][1] = "OFF"
                    str_w[1][3] = "False"
                    str_w = "\n".join([",".join(str_w[0][:]),",".join(str_w[1][:])])
                    #print(str_w)
                    f.write(str_w)
                executor.submit(kill_iperf)
                print("kill iperf")
    
        sleep(4)
        count += 1
    
if  __name__=="__main__":
    main()
