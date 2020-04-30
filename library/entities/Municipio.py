import numpy as np
import matplotlib.pyplot as plt


class Municipio():

    def __init__(self, id_, total_alunos, percentual_alunos_ead, total_docentes, percentual_pop_ativa, total_servidores_publicos,
                 total_servidores_publicos_saude, total_veiculos, tempo_analise):
        self.id = id_
        self.total_alunos = total_alunos
        self.percentual_alunos_ead = percentual_alunos_ead
        self.total_docentes = total_docentes
        self.percentual_pop_ativa = percentual_pop_ativa
        self.percentual_pop_inaativa = 1.0 - self.percentual_pop_ativa
        self.total_servidores_publicos = total_servidores_publicos
        self.total_servidores_publicos_saude = total_servidores_publicos_saude
        self.total_veiculos = total_veiculos
        self.tempo_analise = tempo_analise
        self.aglomerados = list()

    def adicionar_aglomerado(self, novo_aglomerado):
        self.aglomerados.append(novo_aglomerado)

    def __ajustar_aglomerados(self):
        total_habitantes = 0.0
        for ag in self.aglomerados:
            total_habitantes = total_habitantes + ag.total_habitantes
        for ag in self.aglomerados:
            ag.percentual_habitantes = ag.total_habitantes/total_habitantes
            ag.total_servidores_publicos = ag.percentual_habitantes * self.total_servidores_publicos
            ag.total_servidores_publicos_saude = np.ceil(ag.percentual_habitantes * self.total_servidores_publicos_saude)
            ag.total_trabalhadores_informais = ag.total_pop_ativa - ag.total_servidores_publicos - ag.total_servidores_publicos_saude
            ag.total_veiculos = ag.percentual_habitantes * self.total_veiculos
            ag.total_alunos = ag.percentual_habitantes * self.total_alunos
            ag.total_docentes = ag.percentual_habitantes * self.total_docentes
            ag.tempo_analise = self.tempo_analise
            ag.percentual_alunos_ead = self.percentual_alunos_ead

    def calcula_demanda_trafego(self):
        self.__ajustar_aglomerados()
        for ag in self.aglomerados:
            ag.calcula_demanda_trafego()

    def calcula_dimensionamento_rede_acesso(self):
        for ag in self.aglomerados:
            ag.calcula_dimensionamento_rede_acesso()

    def debug(self):
        time = np.arange(self.tempo_analise)
        demanda_trafego_total = np.zeros(self.tempo_analise)
        demanda_usuarios_total = np.zeros(self.tempo_analise)
        demanda_aplicacoes_total = np.zeros(self.tempo_analise)
        for ag in self.aglomerados:
            print('Dados do Aglomerado {}:'.format(ag.id))
            print('User Fraction')
            print(ag.user_fraction)
            print('\n')
            print('Densidade Usuarios')
            print(ag.densidade_usuarios)
            print('\n')
            print('Demanda Tráfego por Terminais')
            print(ag.demanda_trafego_terminais)
            print('\n')
            print('Demanda de Usuários de Internet')
            print(ag.demanda_usuarios)
            demanda_usuarios_total += ag.demanda_usuarios
            print('\n')
            print('Demanda Aplicações')
            print(ag.demanda_aplicacoes)
            demanda_aplicacoes_total += ag.demanda_aplicacoes
            print('\n')
            print('Demanda de Trafego')
            print(ag.demanda_trafego)
            demanda_trafego_total += ag.demanda_trafego
            print('\n')
            plt.title('Demanda de Tráfego x Densidade de Usuários - Aglomerado {}'.format(ag.id))
            plt.plot(ag.densidade_usuarios, ag.demanda_trafego, '-*')
            plt.xlabel('Densidade de Usuários (usuários/km2)')
            plt.ylabel('Demanda de Tráfego [Mbps/km2]')
            plt.grid(linestyle=':')

            plt.figure()
            plt.title('Demanda de Tráfego Total: Aglomerado {}'.format(ag.id))
            plt.plot(time, ag.demanda_trafego, '-*', label='Demada de Tráfego Total')
            plt.plot(time, ag.demanda_usuarios, '-o', label='Demanda Usuários')
            plt.plot(time, ag.demanda_aplicacoes, '-.', label='Demanda Aplicações IoT/M2M')
            plt.xlabel('Período de Análise (t)')
            plt.ylabel('Demanda de Tráfego [Mbps/km2]')
            plt.grid(linestyle=':')
            plt.figure()

        plt.title('Demanda de Tráfego Total do Município')
        plt.plot(time, demanda_trafego_total, '-*', label='Demanda Total')
        plt.plot(time, demanda_usuarios_total, '-o', label='Demanda Usuários')
        plt.plot(time, demanda_aplicacoes_total, '-.', label='Demanda Aplicações IoT/M2M')
        plt.xlabel('Período de Análise (t)')
        plt.ylabel('Demanda de Tráfego [Mbps/km2]')
        plt.grid(linestyle=':')
        plt.legend(loc='upper left')
        plt.show()