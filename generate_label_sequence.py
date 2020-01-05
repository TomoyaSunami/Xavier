import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import correction

def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-r', '--rise_width_size', type=int, default=10)
    parser.add_argument('-f', '--fall_width_size', type=int, default=10)
    args = parser.parse_args()
    main(args.input, args.rise_width_size, args.fall_width_size)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [float(s[1]) for s in l_strip]
    return time, confidence

def main(path,rw_size,fw_size):
    _,array = load_sequence(path)
    array = correction.avg_correction(array,1,0.001)
    print(array)
    rw = [0]*4
    rw.append(1)
    fw = [0]*4
    fw.insert(0,1)
    rise_index = []
    fall_index = []
    for i in range(len(array)-rw_size):
        if array[i:i+rw_size+1] == rw:
            rise_index.append(i+rw_size)
    for i in range(len(array)-fw_size):
        if array[i:i+fw_size+1] == fw:
            fall_index.append(i+1)
    print(rise_index, fall_index)
    if len(rise_index)==0 or len(fall_index)==0:
        sys.exit(0)
    label_array = [0]*len(array)
    if fall_index[0] < rise_index[0]:
        label_array[:fall_index[0]] = [1]*fall_index[0]
        fall_index.pop(0)
    if fall_index[-1] < rise_index[-1]:
        label_array[rise_index[-1]:] = [1]*(len(label_array)-rise_index[-1])
    for i,j in zip(rise_index,fall_index):
        label_array[i:j] = [1]*(j-i)
    plt.plot(array)
    plt.plot(label_array)
    plt.show()
    

if __name__=="__main__":
    execute_cmdline()
