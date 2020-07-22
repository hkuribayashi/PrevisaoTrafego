import math

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from library.entities.central_office import CentralOffice


class Municipio():

    def __init__(self, id_, total_alunos, percentual_alunos_ead, total_docentes, percentual_pop_ativa,
                 total_servidores_publicos, total_servidores_publicos_saude, total_veiculos, tempo_analise,
                 tempo_viagem, tempo_medio_disponibilidade):
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
        self.tempo_viagem = tempo_viagem
        self.tempo_medio_disponibilidade = tempo_medio_disponibilidade
        self.tipos_rede_radio = ['Macro', 'Hetnet']

        self.aglomerados = list()
        self.fibra_otica_implantada = \
            dict(implantacao_macro=np.zeros(tempo_analise), implantacao_hetnet=np.zeros(tempo_analise))
        self.modem_pon_implantado = \
            dict(implantacao_macro=np.zeros(tempo_analise), implantacao_hetnet=np.zeros(tempo_analise))
        self.antena_mw_implantada_pt_pt = \
            dict(implantacao_macro=np.zeros(tempo_analise), implantacao_hetnet=np.zeros(tempo_analise))
        self.sw_carrier_mw_implantada = \
            dict(implantacao_macro=np.zeros(tempo_analise), implantacao_hetnet=np.zeros(tempo_analise))
        self.olt_implantada = \
            dict(implantacao_macro=np.zeros(tempo_analise), implantacao_hetnet=np.zeros(tempo_analise))
        self.sw_agregacao = np.zeros(tempo_analise)
        self.antenas_pt_pt = np.zeros(tempo_analise)

        self.co = CentralOffice()


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
            ag.percentual_pop_ativa = self.percentual_pop_ativa
            ag.total_pop_ativa = ag.percentual_pop_ativa * ag.total_habitantes
            ag.total_trabalhadores_informais = ag.total_pop_ativa - ag.total_servidores_publicos - ag.total_servidores_publicos_saude
            ag.total_veiculos = ag.percentual_habitantes * self.total_veiculos
            ag.total_alunos = ag.percentual_habitantes * self.total_alunos
            ag.total_docentes = ag.percentual_habitantes * self.total_docentes
            ag.total_pop_inativa = ag.total_habitantes - ag.total_pop_ativa
            ag.percentual_alunos_ead = self.percentual_alunos_ead

    def calcula_demanda_trafego(self):
        self.__ajustar_aglomerados()
        temp = np.zeros(self.tempo_analise)
        for ag in self.aglomerados:
            ag.calcula_demanda_trafego()
            temp += ag.total_terminais
        print('Total de Terminais:')
        print(temp)
        print()

    def calcula_dimensionamento_rede_acesso(self):
        for ag in self.aglomerados:
            ag.calcula_dimensionamento_rede_acesso()

    def calcula_dimensionamento_rede_transporte(self):
        # Calcula o transporte dentro de cada aglomerado
        total_macro = 0.0
        total_hetnet = 0.0
        for ag in self.aglomerados:
            total_macro += len(ag.lista_bs['implantacao_macro'])
            total_hetnet += len(ag.lista_bs['implantacao_hetnet'])
            ag.calcula_dimensionamento_rede_transporte()

        '''
        Calculo da quantidade de antenas MW Pt-Pt entre os aglomerados
        Antenas com capacidade de transmissão superior às instaladas dentro dos aglomerados
        Este cálculo depende diretamente da topologia gerada pela AGM
        Para a topologia Sede -> Ubim -> Nova Maracanã temos 02 (duas) arestas que ligam os 03 (três) aglomerados
        Portanto, para cada aresta temos um par de antenas MW pt-pt de alta capacidade, totalizando 04 antenas pt-pt
        de alta capacidade que ligam os aglomerados à sede
        
        O valor calcula será implantado no Ano 0 (zero) e deve ser igual para as duas estretégias (Macro e Hetnet)
        '''
        self.antenas_pt_pt[0] = 2 * 2

        for ag in self.aglomerados:
            # Somatório do quantitativo de Antenas MW pt-pt baixa capacidade (dentro do aglomerado)
            self.antena_mw_implantada_pt_pt['implantacao_macro'] += ag.qtd_antena_mw_macro
            self.antena_mw_implantada_pt_pt['implantacao_hetnet'] += ag.qtd_antena_mw_hetnet

            # Somatório do quantitativo de Antenas MW pt-Mp baixa capacidade (dentro do aglomerado)
            self.sw_carrier_mw_implantada['implantacao_macro'] += ag.qtd_sw_carrier_mw_macro_only
            self.sw_carrier_mw_implantada['implantacao_hetnet'] += ag.qtd_sw_carrier_mw_hetnet

    def calcula_dimensionamento_centraloffice(self):
        print('Dimensionamento de Central Office')
        demanda_trafego_total = np.zeros(self.tempo_analise)

        # Calcula a quantidade de servidores de rede pra rodar as funções de SDN
        servidores_implantados_por_ano_datacenter = np.zeros(self.tempo_analise)
        for ag in self.aglomerados:
            demanda_trafego_total += ag.demanda_trafego_por_area * ag.area_aglomerado

        # A partir da demanda de tráfego total do município é necessário estimar a infraestrutura do micro datacenter
        # Assumindo a capacidade de atendimento de 800 Mbps por servidor
        for ano, demanda_ano in enumerate(demanda_trafego_total):
            if ano == 0:
                servidores_implantados_por_ano_datacenter[ano] = math.ceil(demanda_ano/800)
            else:
                servidores_implantados_por_ano_datacenter[ano] = math.ceil(demanda_ano/800) \
                                                                 - sum(servidores_implantados_por_ano_datacenter[:ano])
        print('Quantidade de Servidores por Ano')
        print(servidores_implantados_por_ano_datacenter)

        '''
        Calcula a quantidade de switches de agregação na opção de transporte por microwave. 
        O total de switches é proporcional ao número de nós não folha, isto é, a qtd de aglomerados que conectam 
        diretamente na sede. Assumindo mais uma vez a topologia Sede -> Ubim -> Nova Maracanã temos apenas 01 aglomerado
        "Nao Folha". Vamos considerar que cada SW de Agregação possui 12 Portas.
        O cálculo é em função da AGM
        '''

        qtd_portas_sw_agregacao = 12
        qtd_aglomerados_nao_folha = 1 # A partir do pressuposto acima, esse aglomerado seria Ubim

        # Na equação abaixo é somado + 1 para considerar a porta utilizada pelas antenas agregadas da Sede
        # Considerar a variável qt_sw_agregacao como atributo da classe Municipio
        qt_sw_agregacao = math.ceil( (qtd_aglomerados_nao_folha + 1)/qtd_portas_sw_agregacao )

        # Todos os SW são implantados no Ano 0, pq dependem da topologia da AGM e não do quantitativo de BS
        # Assim o mesmo valor ou array (self.sw_agregacao) deve ser considerado para as opções de Macro Only e Hetnet
        self.sw_agregacao[0] = qt_sw_agregacao

        print('Quantidade de SW de Agregação MW:')
        print(self.sw_agregacao)

    def gera_graficos_municipio(self):
        time = np.arange(self.tempo_analise)
        demanda_trafego_total = np.zeros(self.tempo_analise)
        demanda_usuarios_total = np.zeros(self.tempo_analise)
        demanda_aplicacoes_total_area = np.zeros(self.tempo_analise)

        capacidade_atendimento_rede_acesso_macro = np.zeros(self.tempo_analise)
        capacidade_atendimento_rede_acesso_femto = np.zeros(self.tempo_analise)
        volume_trafego_rede_acesso_total = np.zeros(self.tempo_analise)

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
            demanda_aplicacoes_total_area += ag.demanda_aplicacoes
            print('\n')
            print('Demanda de Trafego')
            print(ag.demanda_trafego_por_area)
            demanda_trafego_total += ag.demanda_trafego_por_area
            print('\n')

            capacidade_atendimento_rede_acesso_macro += ag.capacidade_atendimento_rede_acesso['implantacao_macro']
            capacidade_atendimento_rede_acesso_femto += ag.capacidade_atendimento_rede_acesso['implantacao_hetnet']
            volume_trafego_rede_acesso_total += ag.demanda_trafego

            plt.title('Demanda de Tráfego por Área x Densidade de Usuários - Aglomerado {}'.format(ag.id))
            plt.plot(ag.densidade_usuarios, ag.demanda_trafego_por_area, '-*')
            plt.xlabel('Densidade de Usuários (usuários/km2)')
            plt.ylabel('Demanda de Tráfego por Área [Mbps/km2]')
            plt.grid(linestyle=':')

            plt.figure()
            plt.title('Demanda de Total de Tráfego por Área: Aglomerado {}'.format(ag.id))
            plt.plot(time, ag.demanda_trafego_por_area, '-*', label='Demada de Tráfego Total')
            plt.plot(time, ag.demanda_usuarios, '-o', label='Demanda Usuários')
            plt.plot(time, ag.demanda_aplicacoes, '-.', label='Demanda Aplicações IoT/M2M')
            plt.xlabel('Período de Análise (t)')
            plt.ylabel('Demanda de Tráfego por Área [Mbps/km2]')
            plt.legend(loc='best')
            plt.grid(linestyle=':')
            plt.figure()

            plt.title('Capacidade de Atendimento Rede de Acesso - Aglomerado {}'.format(ag.id))
            plt.plot(ag.demanda_trafego, ag.capacidade_atendimento_rede_acesso['implantacao_macro'], '-*',
                     label='Capacidade Implantação Macro Only [Mbps]')
            plt.plot(ag.demanda_trafego, ag.capacidade_atendimento_rede_acesso['implantacao_hetnet'], '-o',
                     label='Capacidade Implantação HetNet [Mbps]')
            plt.xlabel('Volume de Tráfego de Dados do Aglomerado [Mbps]')
            plt.ylabel('Capacidade de Atendimento [Mbps]')
            plt.grid(linestyle=':')
            plt.legend(loc='best')
            plt.figure()

            plt.title('Capacidade de Atendimento Rede de Acesso - Aglomerado {}'.format(ag.id))
            plt.plot(time, ag.capacidade_atendimento_rede_acesso['implantacao_macro'], '-*',
                     label='Capacidade Implantação Macro Only [Mbps]')
            plt.plot(time, ag.capacidade_atendimento_rede_acesso['implantacao_hetnet'], '-o',
                     label='Capacidade Implantação HetNet [Mbps]')
            plt.plot(time, ag.demanda_trafego, '-.', label='Volume de Tráfego [Mbps]')
            plt.xlabel('Período de Análise (t)')
            plt.ylabel('Capacidade de Atendimento [Mbps]')
            plt.grid(linestyle=':')
            plt.legend(loc='best')
            plt.figure()

        plt.title('Demanda de Total de Tráfego por Área  do Município {}'.format(self.id))
        plt.plot(time, demanda_trafego_total, '-*', label='Demanda Total')
        plt.plot(time, demanda_usuarios_total, '-o', label='Demanda Usuários')
        plt.plot(time, demanda_aplicacoes_total_area, '-.', label='Demanda Aplicações IoT/M2M')
        plt.xlabel('Período de Análise (t)')
        plt.ylabel('Demanda de Tráfego por Área [Mbps/km2]')
        plt.grid(linestyle=':')
        plt.legend(loc='upper left')
        plt.figure()

        plt.title('Capacidade de Atendimento Rede de Acesso - Municipio {}'.format(self.id))
        plt.plot(time, capacidade_atendimento_rede_acesso_macro, '-*',
                 label='Capacidade Implantação Macro Only [Mbps]')
        plt.plot(time, capacidade_atendimento_rede_acesso_femto, '-o',
                 label='Capacidade Implantação HetNet [Mbps]')
        plt.plot(time, volume_trafego_rede_acesso_total, '-.', label='Volume de Tráfego [Mbps]')
        plt.xlabel('Período de Análise (t)')
        plt.ylabel('Capacidade de Atendimento [Mbps]')
        plt.grid(linestyle=':')
        plt.legend(loc='best')
        plt.show()
