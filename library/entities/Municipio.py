import numpy as np
import matplotlib.pyplot as plt


class Municipio():

    contador_id = 0

    def __init__(self, id_, total_alunos, percentual_ead, total_docentes, percentual_pop_ativa, total_servidores_publicos,
                 total_servidores_publicos_saude, total_veiculos, tempo_analise):
        self._id = id_
        self._total_alunos = total_alunos
        self._percentual_ead = percentual_ead
        self._total_docentes = total_docentes
        self._percentual_pop_ativa = percentual_pop_ativa
        self._percentual_pop_inaativa = 1.0 - self._percentual_pop_ativa
        self._total_servidores_publicos = total_servidores_publicos
        self._total_servidores_publicos_saude = total_servidores_publicos_saude
        self._total_veiculos = total_veiculos
        self._tempo_analise = tempo_analise
        self._aglomerados = list()

    @property
    def percentual_pop_ativa(self):
        return self._percentual_pop_ativa

    def adicionar_aglomerado(self, novo_aglomerado):
        self.contador_id += 1
        novo_aglomerado.id = self.contador_id
        self._aglomerados.append(novo_aglomerado)

    def __ajustar_aglomerados(self):
        total_habitantes = 0.0
        for ag in self._aglomerados:
            total_habitantes = total_habitantes + ag.total_habitantes
        for ag in self._aglomerados:
            ag.percentual_habitantes = ag.total_habitantes/total_habitantes
            ag.total_servidores_publicos = ag.percentual_habitantes * self._total_servidores_publicos
            ag.total_servidores_publicos_saude = ag.percentual_habitantes * self._total_servidores_publicos_saude
            ag.total_trabalhadores_informais = ag.total_pop_ativa - ag.total_servidores_publicos - ag.total_servidores_publicos_saude
            ag.total_veiculos = ag.percentual_habitantes * self._total_veiculos
            ag.tempo_analise = self._tempo_analise

    def calcula_demanda_trafego(self):
        self.__ajustar_aglomerados()
        for ag in self._aglomerados:
            ag.calcula_demanda_trafego()

    def calcula_dimensionamento_rede_acesso(self):
        for ag in self._aglomerados:
            ag.calcula_dimensionamento_rede_acesso()

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