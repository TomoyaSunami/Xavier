
"""
load the result of object detection and build hmm
"""

import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import joblib


def load_sequence(path):

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
    x = [int(s) for s in l_strip]
    x = np.array(x)    
    return x

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

def plot_graph(X1, X2):
    plt.subplot(2,1,1)
    plt.subplots_adjust(hspace=1)
    plt.plot(X1)
    #plt.title("train observed sequence")
    plt.xlabel('Index')
    plt.yticks((0,1))
    
    plt.subplot(2,1,2)
    plt.subplots_adjust(hspace=1)
    plt.plot(X2)
    #plt.title("train estimated state")
    plt.xlabel('Index')
    plt.yticks((0,1))

    plt.show()

def main():
    
    output_sequence = load_sequence("output_sequence.txt")
    #model = hmm.MultinomialHMM(n_components=2,n_iter=10000)
    model = hmm.GaussianHMM(n_components=2,n_iter=10000)
    
    model.fit(output_sequence.reshape(len(output_sequence),1))
    joblib.dump(model, "HMM.pkl")

    x_array = np.empty([1,0],int)
    hmm_estimation = 0
    estimated_state = []
    for x in output_sequence:
        x_array = stock(x_array, x, 10)
        

        hmm_estimation = hmm_estimate(model, x_array, hmm_estimation)
        estimated_state.append(hmm_estimation)

    plot_graph(output_sequence, estimated_state)

    

if __name__ == "__main__":
    main()

