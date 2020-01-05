import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

import joblib
import correction

def load_sequence(path):
    if not os.path.exists(path):
        print(path, 'does not exist')
        sys.exit(1)
    with open(path,'r') as f:
        l_strip = [s.strip().split(",") for s in f.readlines()]
        time = [float(s[0]) for s in l_strip]
        confidence = [float(s[1]) for s in l_strip]
    return time, confidence

def hmm_predict(avg_confidence):
    model = joblib.load("HMM_1215.pkl")

    x_array = np.empty([1,0],int)
    hmm_estimation = 0
    estimated_state = []
    for x in avg_confidence:
        x_array = correction.stock(x_array, x, 10)
        
        hmm_estimation = correction.hmm_estimate(model, x_array, hmm_estimation)
        estimated_state.append(hmm_estimation)
    return estimated_state

def main():
    window_size = [1,2,3,4,5,10]
    threshold = [0.001,0.01,0.05,0.1,0.15,0.2,0.25]
    wt = np.zeros([len(window_size),len(threshold)])
    time,array = load_sequence("0106/yolo_output3_sampling.txt")
    _,label_array = load_sequence("0106/yolo_output3_sampling_label.txt")
    for i,w in enumerate(window_size):
        for j,th in enumerate(threshold):
            avg_array = correction.avg_correction(array,w,th)
            hmm_array = hmm_predict(avg_array)
            avg_acc = (len(avg_array) - sum(np.logical_xor(avg_array,label_array))) / len(avg_array)
            hmm_acc = (len(hmm_array) - sum(np.logical_xor(hmm_array,label_array))) / len(hmm_array)

            wt[i,j] = hmm_acc
            
    print(wt)

    fig,ax = plt.subplots()
    ax.set_xlabel("threshold")
    ax.set_ylabel("window size")
    ax.set_xticks([0,1,2,3,4,5,6])
    ax.set_yticks([5,4,3,2,1,0])
    ax.set_yticklabels(window_size)
    ax.set_xticklabels(["0","0.01","0.05","0.1","0.15","0.2","0.25"])
    plt.imshow(wt,cmap="coolwarm")
    pp = plt.colorbar() 
    plt.show()


if __name__=="__main__":
    main()
