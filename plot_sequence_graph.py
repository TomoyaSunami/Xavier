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
    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        x = [int(s) for s in l_strip]
    return x


def plot_graph(paths):
    fig, axes = plt.subplots(len(paths),1)
    if len(paths) == 1:
        axes = [axes]
    hspace = 0.5 * len(paths)
    for path, ax in zip(paths, axes):
        x = load_sequence(path)
        ax.plot(range(len(x)),x)
        #ax.set_yticks([0,1])
        ax.set_xlabel("Index")
        plt.subplots_adjust(hspace=hspace)
    plt.show()
    

if __name__=="__main__":
    execute_cmdline()
