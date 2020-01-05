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
    parser.add_argument('-w', '--window_size', type=int, default=5)
    parser.add_argument('-th','--threshold', type=float, default=0.05)
    parser.add_argument('-g', '--graph', action='store_true')
    parser.add_argument('-avg','--only_avg', action='store_true') 
    args = parser.parse_args()
    main(args.input, args.window_size, args.threshold, args.graph, args.only_avg)

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [float(s[1]) for s in l_strip]
    return time, confidence

def avg_correction(confidence,window_size, threshold):
    df = pd.Series(confidence)
    df = df.rolling(window_size, min_periods=1).mean()
    confidence = df.to_numpy()
    confidence = np.where(confidence < threshold, 0, 1)
    return confidence

def stock(x_array, x, window_size):
    length = len(x_array)   
    if length < window_size:
        x_array = np.append(x_array,x)
    else :
        x_array = np.roll(x_array, -1)
        x_array[-1] = x  
    return x_array

def hmm_estimate(model, observed_sequence, pre_estimation):
    if len(observed_sequence) <= 1:
        return 0
    observed_sequence = np.array([observed_sequence]).T

    logprob,state_sequence = model.decode(observed_sequence)
    
    if model.emissionprob_[0,0] > model.emissionprob_[0,1] and model.emissionprob_[1,0] < model.emissionprob_[1,1]:
        estimation = 0 if state_sequence[-1] == 0 else 1
    elif model.emissionprob_[0,0] < model.emissionprob_[0,1] and model.emissionprob_[1,0] > model.emissionprob_[1,1]:
        estimation = 1 if state_sequence[-1] == 0 else 0
    else:
        estimation = pre_estimation

    return estimation

def plot_graph(*array):
    fig, axes = plt.subplots(len(array),1)
    if len(array) == 1:
        axes = [axes]
    hspace = 0.5 * len(array)
    for ar, ax in zip(array, axes):
        ax.plot(ar)
        #ax.set_yticks([0,1])
        ax.set_xlabel("Time")
        plt.subplots_adjust(hspace=hspace)
    plt.show()

def save_sequence(path,time,confidence):
    str_w = ""
    for t,c in zip(time,confidence):
        str_w += str(t)+","+str(c)+"\n"
    
    with open(path,'w') as f:
        f.write(str_w)

def main(path,window,threshold,graph,only_avg):
    time, confidence = load_sequence(path)
    avg_confidence = avg_correction(confidence,window,threshold)
    
    if only_avg:
        save_sequence(path.replace(".txt","_avg.txt"),time,avg_confidence)
        sys.exit(0)

    model = joblib.load("test-HMM.pkl")

    x_array = np.empty([1,0],int)
    hmm_estimation = 0
    estimated_state = []
    for x in avg_confidence:
        x_array = stock(x_array, x, 10)
        
        hmm_estimation = hmm_estimate(model, x_array, hmm_estimation)
        estimated_state.append(hmm_estimation)
    
    save_sequence(path.replace(".txt","_correct.txt"),time,estimated_state)

    if graph : plot_graph(confidence,avg_confidence,estimated_state)


if __name__=="__main__":
    execute_cmdline()