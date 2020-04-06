import numpy as np


def get_gompertz(mu=0.4, gamma=0.2, total_time=15):
    beta = np.log(2)
    h = np.zeros(total_time)
    for t in range(total_time):
        temp = (-1.0 * beta) * np.exp(-1.0 * gamma * t)
        h[t] = mu * np.exp(temp)
    return h
