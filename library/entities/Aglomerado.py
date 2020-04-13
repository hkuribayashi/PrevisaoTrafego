import numpy as np
import matplotlib.pyplot as plt

from library.entities.Aplicacacao import Aplicacao
from library.util.Util import get_gompertz


class Aglomerado:

    def __init__(self, area, densidade_populacional, tempo_analise, populacao_ativa, numero_terminais_educacao,
                 numero_terminais_saude, numero_terminais_comercio, numero_terminais_governanca,
                 numero_terminais_seguranca, proporcao_final_terminais_heavy, taxa_crescimento_terminais_heavy,
                 proporcao_final_usuario_internet, taxa_crescimento_usuarios_internet, taxa_usuarios_ativos):

        self._area = area
        self._densidade_populacional = densidade_populacional
        self._numero_terminais_educacao = numero_terminais_educacao
        self._numero_terminais_saude = numero_terminais_saude
        self._numero_terminais_comercio = numero_terminais_comercio
        self._numero_terminais_governanca = numero_terminais_governanca
        self._numero_terminais_seguranca = numero_terminais_seguranca
        self._populacao_ativa = populacao_ativa # representa a parcela economicamente ativa da população
        self._tempo_analise = tempo_analise
        self._proporcao_final_terminais_heavy = proporcao_final_terminais_heavy # mi/determina a taxa final de adoção de terminais do tipo heavy
        self._taxa_crescimento_terminais_heavy = taxa_crescimento_terminais_heavy # gamma/taxa de adoção dos terminais do tipo j
        self._proporcao_final_usuario_internet = proporcao_final_usuario_internet #mu/determina a taxa final de adoção de internet por usuário
        self._taxa_crescimento_usuarios_internet = taxa_crescimento_usuarios_internet #gamma/taxa de adocao de internet
        self._taxa_usuarios_ativos = taxa_usuarios_ativos

        self._demanda_trafego = 0.0
        self._densidade_usuarios = 0.0
        self._demanda_trafego_terminais = 0.0
        self._demanda_usuarios = 0.0
        self._demanda_aplicacoes = 0.0
        self._user_fraction = 0.0

    @property
    def area(self):
        return self._area

    @property
    def densidade_populacional(self):
        return self._densidade_populacional

    @property
    def populacao_ativa(self):
        return self._populacao_ativa

    @property
    def demanda_trafego(self):
        return self._demanda_trafego

    def calcula_demanda_aplicacoes(self):
        demanda_aplicacoes = np.zeros(self._tempo_analise)
        for app in Aplicacao:
            c = get_gompertz(1.0, app.value['start_adoption'], app.value['adoption_rate'], self._tempo_analise)
            c = (app.value['estimated_quantity']/self._area) * c
            demanda_aplicacoes += c
        self._demanda_aplicacoes = demanda_aplicacoes

    def calcula_densidade_usuarios(self):
        densidade_usarios = get_gompertz(self._proporcao_final_usuario_internet, 5, self._taxa_crescimento_usuarios_internet, self._tempo_analise)
        self._densidade_usuarios = densidade_usarios * self._densidade_populacional * self._populacao_ativa

    def calcula_trafego_terminal(self):
        # Inicializa duas matrizes com 3 linhas (tipos de terminais) x 'tempo_analise' colunas
        r_j = np.zeros((3, self._tempo_analise))
        rs_j = np.zeros((3, self._tempo_analise))

        heavy_users = get_gompertz(self._proporcao_final_terminais_heavy, 5, self._taxa_crescimento_terminais_heavy, self._tempo_analise)
        heavy_users = np.array([heavy_users]) # ela era um array e converteu ele em uma matriz de uma linha
        ordinary_users = 1 - heavy_users # ele cria uma matriz ordinary para receber o resultado da subtracao entre 1 e o primeiro, segundo... elemento da matriz heavy e coloca o resultado na respectiva posicao da matriz ordinary

        self._user_fraction = np.concatenate((heavy_users, ordinary_users), axis=0)

        # Linhas: r_heavy/rordinary; Colunas: PC/Tablets/Smartphones
        # Valores expressos em Mbps
        # demanda_trafego_terminais = np.array([[0.125, 0.06244444, 0.01562222], [0.031, 0.00780556, 0.00195278]])
        demanda_trafego_terminais = np.array([[25.0, 5.0, 2.0], [3.125, 0.625, 0.25]]) # valores aumentados

        for i in range(self._tempo_analise):
            r_j[:, i] = np.asmatrix(self._user_fraction[:, i].T).dot(demanda_trafego_terminais)

        # Proporção entre terminais PC/Tablets/Smartphones
        # Valores: 20%/10%/70%
        s_j = np.array([[0.2, 0.1, 0.7]])

        # Multiplica ponto-a-ponto cada coluna de r_j por s_j
        for i in range(self._tempo_analise):
            rs_j[:, i] = np.multiply(r_j[:, i], s_j)

        self._demanda_trafego_terminais = np.sum(rs_j, axis=0) # achata somando as linhas, resultado em 1 linha e 15 colunas

    def calcula_demada_usuarios(self):
        self._demanda_usuarios = self._densidade_usuarios * self._taxa_usuarios_ativos *self._demanda_trafego_terminais

    def calcula_demanda_trafego(self):
        self.calcula_demanda_aplicacoes()
        self.calcula_densidade_usuarios()
        self.calcula_trafego_terminal()
        self.calcula_demada_usuarios()
        self._demanda_trafego = np.add(self._demanda_aplicacoes, self._demanda_usuarios) # faco um chuveirinho somando

    def debug(self):
        print('User Fraction')
        print(self._user_fraction)
        print('\n')
        print('Densidade Usuarios')
        print(self._densidade_usuarios)
        print('\n')
        print('Demanda Tráfego por Terminais')
        print(self._demanda_trafego_terminais)
        print('\n')
        print('Demanda de Usuários de Internet')
        print(self._demanda_usuarios)
        print('\n')
        print('Demanda Aplicações')
        print(self._demanda_aplicacoes)
        print('\n')
        print('Demanda de Trafego')
        print(self._demanda_trafego)

        time = np.arange(self._tempo_analise)

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Período de Análise (t)')
        ax1.set_ylabel('Demanda de Tráfego [Mbps/km2]', color=color)
        ax1.plot(time, self._demanda_trafego, '-.', color=color)
        ax1.grid(linestyle=':')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()

        color = 'tab:blue'
        ax2.set_ylabel('Densidade de Usuários [usuários/km2]', color=color)
        ax2.plot(time, self._densidade_usuarios, '-*', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.show()

        plt.plot(self._densidade_usuarios, self._demanda_trafego, '-*')
        plt.xlabel('Densidade de Usuários [usuários/km2]')
        plt.ylabel('Demanda de Tráfego [Mbps/km2]')
        plt.grid(linestyle=':')
        plt.show()
