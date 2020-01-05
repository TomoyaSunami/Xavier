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

def main(input):
    



if __name__=="__main__":
    main()
