import numpy
import argparse
import os
import sys
import subprocess
from concurrent.futures import ProcessPoolExecutor
import time

def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-f', '--fps', type=float)
    parser.add_argument('-g', '--graph', action='store_true')    
    args = parser.parse_args()
    main(args.input,args.fps,args.graph)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [int(s[1]) for s in l_strip]
    return time, confidence

def start(time):
    cmd = "iperf -t 60 -c 192.168.0.3 -t " + str(time)
    proc = subprocess.Popen(cmd.split(" "))

def save_sequence(path,time,confidence):
    str_w = ""
    for t,c in zip(time,confidence):
        str_w += str(t)+","+str(c)+"\n"
    
    with open(path,'w') as f:
        f.write(str_w)


def main(path,fps,graph):
    _,timing = load_sequence(path)
    
    elapsed_time = 0
    eps = 0.001
    target_time = 1/fps
    for i in timing:
        start_time = time.time()
        
        if i != 0:
            start(i)
        elapsed_time = time.time() - start_time
        while abs(target_time-elapsed_time)>eps:
            time.sleep(0.001)
            elapsed_time = time.time() - start_time

if __name__=="__main__":
    execute_cmdline()