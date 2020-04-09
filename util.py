import numpy as np


def get_gompertz(mu, beta, gamma, total_time):
    h = np.zeros(total_time)
    for t in range(total_time):
        temp = -beta * np.exp(-gamma * t)
        h[t] = mu * np.exp(temp)
    return h