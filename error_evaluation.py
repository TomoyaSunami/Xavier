import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', type=str)
    args = parser.parse_args()
    print(args.input)
    main(args.input)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [int(s[1]) for s in l_strip]
    return time, confidence

def calc_error(x_hat_array,x_array):
    alpha = sum([x_hat*x for x_hat,x in zip(x_hat_array,x_array)]) / sum([x**2 for x in x_array])
    error = sum([(x_hat - alpha*x)**2 for x_hat,x in zip(x_hat_array,x_array)])
    return error

def main(input_path):
    _,x = load_sequence(input_path[0])
    _,x_hat = load_sequence(input_path[1])
    error = calc_error(x_hat,x)
    



if __name__=="__main__":
    main()