
import numpy as np
import matplotlib.pyplot as plt

# 偏りのないコイン
"""
X = np.empty((0,1), int)
for i in range(0,100):
    X = np.append(X, np.array([[np.random.binomial(1, p=0.5)]]),axis=0)
plt.plot(X)
plt.xlabel('Trial')
plt.yticks((0,1))
plt.show()
"""
plt.figure(figsize=(3, 4))

# 偏りのあるコイン
X = np.empty((0,1), int)
for i in range(0,50):
    X = np.append(X, np.array([[np.random.binomial(1, p=0.9)]]),axis=0)
for i in range(0,50):
    X = np.append(X, np.array([[np.random.binomial(1, p=0.1)]]),axis=0)
plt.subplot(2,1,1)
plt.plot(X)
#plt.xlabel('Trial')
plt.yticks((0,1))


from hmmlearn import hmm
model = hmm.MultinomialHMM(n_components=2,n_iter=50)
model.fit(X)
L,Z = model.decode(X)
plt.subplot(2,1,2)
plt.plot(Z)
#plt.xlabel('Trial')
plt.yticks((0,1))
plt.show()

#emissionprob = model.emissionprob_.reshape(1,4)[0]

#print(emissionprob)

if model.emissionprob_[0,0] < model.emissionprob_[0,1] and model.emissionprob_[1,0] > model.emissionprob_[1,1]:
    if Z[-1] == 0:
        prediction = 1
    else:
        prediction = 0
elif model.emissionprob_[0,0] > model.emissionprob_[0,1] and model.emissionprob_[1,0] < model.emissionprob_[1,1]:
    if Z[-1] == 0:
        prediction = 0
    else:
        prediction = 1

print(model.emissionprob_)

print(prediction)
print(model.predict([[1]]))

def hmm_predict(X):
    from hmmlearn import hmm
    model = hmm.MultinomialHMM(n_components=2,n_iter=50)
    model.fit(X)
    L,Z = model.decode(X)

    if model.emissionprob_[0,0] < model.emissionprob_[0,1] and model.emissionprob_[1,0] > model.emissionprob_[1,1]:
        if Z[-1] == 0:
            prediction = 1
        else:
            prediction = 0
    elif model.emissionprob_[0,0] > model.emissionprob_[0,1] and model.emissionprob_[1,0] < model.emissionprob_[1,1]:
        if Z[-1] == 0:
            prediction = 0
        else:
            prediction = 1

    return prediction

