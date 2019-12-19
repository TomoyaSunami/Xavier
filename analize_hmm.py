
"""

load the result of object detection and build hmm


"""

import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import joblib


def load_binary_series(path):

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        x = [[int(s)] for s in l_strip]

    return x

def generate_binary_series(seed=0, p0=0.1,p1=0.9):
    np.random.seed(seed=seed)
    X = np.empty((0,1), int)
    Y = np.empty((0,1), int)
    random_range = np.random.choice(2,10)
    
    for r in random_range:
        if r:
            for i in range(0,50):
                X = np.append(X, np.array([[np.random.binomial(1, p=p1)]]),axis=0)
                Y = np.append(Y, 1)
        else:
            for i in range(0,50):
                X = np.append(X, np.array([[np.random.binomial(1, p=p0)]]),axis=0)
                Y = np.append(Y, 0)

    return X,Y

def plot_graph(X1, X2, X3,Y1, X4):
    plt.subplot(4,1,1)
    plt.subplots_adjust(hspace=2)
    plt.plot(X1)
    plt.title("train_binary data")
    plt.xlabel('Trial')
    plt.yticks((0,1))
    
    plt.subplot(4,1,2)
    plt.subplots_adjust(hspace=2)
    plt.plot(X2)
    plt.title("train estimated state")
    plt.xlabel('Trial')
    plt.yticks((0,1))

    plt.subplot(4,1,3)
    plt.subplots_adjust(hspace=2)
    plt.plot(X3)
    plt.plot(Y1,linestyle='dashed')
    plt.title("test_binary data")
    plt.xlabel('Trial')
    plt.yticks((0,1))
    
    plt.subplot(4,1,4)
    plt.subplots_adjust(hspace=2)
    plt.plot(X4)
    plt.title("test estimated state")
    plt.xlabel('Trial')
    plt.yticks((0,1))

    plt.show()

def main():



    
    train_binary_series = load_binary_series("train_detected_series_normal.txt")
    model = hmm.MultinomialHMM(n_components=2,n_iter=10000)
    
    model.fit(train_binary_series)
    joblib.dump(model, "HMM_normal.pkl")

    
    test_binary_series, y = generate_binary_series()

    model = joblib.load('HMM_normal.pkl')
    
    train_L,train_prediction = model.decode(train_binary_series)
    L,prediction = model.decode(test_binary_series)

    plot_graph(train_binary_series, train_prediction, test_binary_series, y, prediction)

    


if __name__ == "__main__":
    main()
