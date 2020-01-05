import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib


def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-g', '--graph', action='store_true')    
    args = parser.parse_args()
    main(args.input, args.graph)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [int(s[1]) for s in l_strip]
    return time, confidence

def save_sequence(path,time,confidence):
    str_w = ""
    for t,c in zip(time,confidence):
        str_w += str(t)+","+str(c)+"\n"
    
    with open(path,'w') as f:
        f.write(str_w)

def calc_iperf_time(array):
    count = 0
    start_idx = 0
    a = [0]*len(array)
    for i,x in enumerate(array):
        if x == 1:
            if count == 0:
                start_idx = i
            count += 1
            if i == len(array)-1:
                a[start_idx] = count
        if x == 0 and count != 0:
            a[start_idx] = count
            count = 0
    return a

def main(path,graph):
    time, confidence = load_sequence(path)
    #confidence = confidence[70:100]
    #print(confidence)
    iperf_controler = calc_iperf_time(confidence)
    #print(iperf_controler)
    save_sequence(path.replace(".txt","iperf.txt"),time,iperf_controler)



if __name__=="__main__":
    execute_cmdline()