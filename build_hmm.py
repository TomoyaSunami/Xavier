
"""
load the result of object detection and build hmm
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import joblib
import correction

def execute_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    args = parser.parse_args()
    main(args.input)

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

def plot_graph(X1, X2, X3):
    plt.subplot(3,1,1)
    plt.subplots_adjust(hspace=1)
    plt.plot(X1)
    plt.title("observed sequence")
    plt.xlabel('Index')
    plt.yticks((0,1))
    
    plt.subplot(3,1,2)
    plt.subplots_adjust(hspace=1)
    plt.plot(X2)
    plt.title("estimated state sequence (window=all)")
    plt.xlabel('Index')
    plt.yticks((0,1))
    
    plt.subplot(3,1,3)
    plt.subplots_adjust(hspace=1)
    plt.plot(X3)
    plt.title("estimated state sequence (window=10)")
    plt.xlabel('Index')
    plt.yticks((0,1))
    plt.show()

def main(path):
    
    time, confidence = correction.load_sequence(path)
    confidence = correction.avg_correction(confidence,3,0.01)
    model = hmm.MultinomialHMM(n_components=2,n_iter=10000)
    model.fit(confidence.reshape(len(confidence),1))
    joblib.dump(model, "test-HMM.pkl")
    z = model.predict(confidence.reshape(len(confidence),1))

    x_array = np.empty([1,0],int)
    hmm_estimation = 0
    estimated_state = []
    for x in confidence:
        x_array = stock(x_array, x, 700)
        
        hmm_estimation = hmm_estimate(model, x_array, hmm_estimation)
        estimated_state.append(hmm_estimation)

    plot_graph(confidence,z,estimated_state)

    

if __name__=="__main__":
    execute_cmdline()
