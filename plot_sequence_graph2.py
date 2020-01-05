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
    plot_graph(args.input)


def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [float(s[1]) for s in l_strip]
    return time, confidence


def plot_graph(paths):
    fig, axes = plt.subplots(len(paths),1)
    if len(paths) == 1:
        axes = [axes]
    hspace = 0.5 * len(paths)
    for path, ax in zip(paths, axes):
        _,y = load_sequence(path)
        ax.plot(range(len(y)),y)
        #ax.set_yticks([0,1])
        #ax.set_xlabel("Time")
        plt.subplots_adjust(hspace=hspace)
    plt.show()
    

if __name__=="__main__":
    execute_cmdline()
