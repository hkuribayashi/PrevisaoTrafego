import numpy as np


def get_gompertz(mu, beta, gamma, total_time):
    h = np.zeros(total_time)
    for t in range(total_time):
        temp = -beta * np.exp(-gamma * t)
        h[t] = mu * np.exp(temp)
    return h


def get_total_bs(lista_bs):
    total_macro = 0.0
    total_femto = 0.0
    for bs in lista_bs:
        if bs.tipo_BS.tipo == 'Macro':
            total_macro += 1
        else:
            total_femto += 1
