import os
import sys
import argparse
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-f', '--fps', type=float)
    parser.add_argument('-g', '--graph', action='store_true')
    args = parser.parse_args()
    sampling(args.fps, args.input, args.graph)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [float(s[1]) for s in l_strip]
    return time, confidence

def save_sequence(path,time,confidence):
    str_w = ""
    for t,c in zip(time,confidence):
        str_w += str(t)+","+str(c)+"\n"
    
    with open(path,'w') as f:
        f.write(str_w)
    


def sampling(fps,path,graph):
    time, confidence = load_sequence(path)

    x_inter = np.arange(min(time), max(time), 1/fps)
    fitted_curve = interpolate.interp1d(time, confidence, kind="linear")
    y_inter = fitted_curve(x_inter)
    save_sequence(path.replace(".txt","_sampling.txt"),x_inter, y_inter)
    if graph:
        plt.plot(time, confidence, label="row data" ,marker=".", markersize=10)
        plt.plot(x_inter, y_inter, label="interpolated data" , alpha=0.7, marker="s", markersize=5)
        plt.legend()
        plt.show()



if __name__=="__main__":
    execute_cmdline()