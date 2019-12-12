import sys
import os
import getopt
import numpy as np
import matplotlib.pyplot as plt


def load_binary_series(path):

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        x = [[int(s)] for s in l_strip]

    return x

def plot_graph(X):

    plt.subplot(1,1,1)
    plt.plot(X)
    plt.yticks((0,1))
    plt.show()

def main(argv):

    fps = 10


    help_str = 'plot_serie_graph.py -i <input_path> '
    try:
        opts, args = getopt.getopt(argv, 'i:', ['input='])
    except getopt.GetoptError as err:
        print(str(err))
        print(help_str)
        sys.exit(1)
    for opt,arg in opts:
        if opt in ("-i", "--input"):
            input_path = arg


    if not os.path.exists(input_path):
        print(input_path, 'does not exist')
        sys.exit(1)

    
    series = load_binary_series(input_path)
    plot_graph(series)


if __name__ == "__main__":
    main(sys.argv[1:])
