import random
import numpy as np
import matplotlib.pyplot as plt

from library.entities.Ponto import Ponto


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


def get_distancia_euclidiana(bs_a, bs_b):
    return bs_a.ponto.get_distancia_euclidiana(bs_b.ponto)


def get_distancia_manhattan(bs_a, bs_b):
    return bs_a.ponto.get_distancia_manhattan(bs_b.ponto)


def get_ponto_aleatorio():
    x = random.uniform(200.0, 500.0)
    y = random.uniform(200.0, 500.0)
    return Ponto(x, y)


def busca_bs_nao_hub(lista_bs, ano):
    result = list()
    for bs in lista_bs:
        if bs.hub_bs is False and bs.ano == ano:
            result.append(bs)
    return result


def busca_bs_hub(lista_bs):
    for bs in lista_bs:
        if bs.hub_bs is True:
            return bs


def variacao_preco_linear(capital, taxa, periodo):
    montante = np.zeros(periodo)
    for ano in range(len(montante)):
        montante[ano] = capital * (1+taxa)**ano
    return montante


def variacao_preco_composto(capital, taxa, periodo):
    montante = np.zeros(periodo)
    for ano in range(len(montante)):
        if ano == 0:
            montante[ano] = capital
        else:
            montante[ano] = capital + (taxa * montante[ano-1])
    return montante
