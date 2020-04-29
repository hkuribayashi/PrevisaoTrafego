import numpy as np
import copy as cp

from library.entities.Aplicacacao import Aplicacao
from library.hetnet.TrafegoUsuariosMoveis import TrafegoUsuariosMoveis as TUM
from library.hetnet.BSType import BSType
from library.hetnet.BS import BS
from library.util.Util import get_gompertz


class Aglomerado:

    def __init__(self, id_, total_habitantes, area_aglomerado, total_agencias_bancarias, total_domicilios,
                 percentual_pop_ativa, total_cruzamentos):
        self.id = id_
        self.total_habitantes = total_habitantes
        self.area_aglomerado = area_aglomerado
        self.total_agencias_bancarias = total_agencias_bancarias
        self.total_domicilios = total_domicilios
        self.densidade_demografica = total_habitantes/area_aglomerado
        self.percentual_pop_ativa = percentual_pop_ativa
        self.total_pop_ativa = self.percentual_pop_ativa * self.total_habitantes
        self.total_pop_inativa = self.total_habitantes - self.total_pop_ativa
        self.total_cruzamentos = total_cruzamentos

        self.total_servidores_publicos = 0.0
        self.total_servidores_publicos_saude = 0.0
        self.total_trabalhadores_informais = 0.0
        self.total_alunos = 0.0
        self.total_docentes = 0.0
        self.total_veiculos = 0.0
        self.tempo_analise = 0
        self.percentual_alunos_ead = 0.0

        self.percentual_habitantes = 0.0
        self.demanda_trafego = 0.0
        self.densidade_usuarios = 0.0
        self.demanda_trafego_terminais = 0.0
        self.demanda_usuarios = 0.0
        self.demanda_aplicacoes = 0.0
        self.user_fraction = 0.0
        self.tempo_maturacao = 3.0
        self.lista_bs = dict(implantacao_macro = list(), implantacao_femto = list())

    def adicionar_BS(self, BS):
        self.lista_bs['implantacao_macro'].append(BS)
        self.lista_bs['implantacao_femto'].append(cp.deepcopy(BS))

    def calcula_demanda_aplicacoes(self):
        demanda_aplicacoes = np.zeros(self.tempo_analise)
        print('Dados de Aplicações de IoT/M2M para o Aglomerado {}'.format(self.id))
        for app in Aplicacao:
            qtd_terminais = 0.0
            if app.id == 1:
                qtd_terminais = self.total_habitantes
            else:
                if app.id == 2:
                    qtd_terminais = np.ceil(self.total_habitantes/1000.0)
                else:
                    if app.id == 3:
                        qtd_terminais = self.total_servidores_publicos_saude
                    else:
                        if app.id == 4:
                            qtd_terminais = np.ceil(self.total_alunos * self.percentual_alunos_ead)
                        else:
                            if app.id == 5:
                                qtd_terminais = np.ceil(self.total_alunos + self.total_docentes)
                            else:
                                if app.id == 6:
                                    qtd_terminais = self.total_cruzamentos
                                else:
                                    if app.id == 7:
                                        qtd_terminais = np.ceil(self.total_servidores_publicos)
                                    else:
                                        if app.id == 8:
                                            qtd_terminais = self.total_agencias_bancarias * 5
                                        else:
                                            if app.id ==9:
                                                qtd_terminais = np.ceil(self.total_pop_ativa -
                                                                        self.total_servidores_publicos -
                                                                        self.total_servidores_publicos_saude)
                                            else:
                                                if app.id == 10 or app.id == 11:
                                                    qtd_terminais = self.total_domicilios
                                                else:
                                                    qtd_terminais = np.ceil(self.total_veiculos)
            c = get_gompertz(app.mu, app.beta, app.gamma, self.tempo_analise)
            c = (qtd_terminais/self.area_aglomerado) * app.alpha * c * app.vazao
            print('Aplicação IoT: {} (alpha={}, beta={}, mu={}, gamma={}, terminais={}, vazao={})'.format(app.nome, app.alpha, app.beta, app.mu, app.gamma, qtd_terminais, app.vazao))
            demanda_aplicacoes += c
        self.demanda_aplicacoes = demanda_aplicacoes
        print()

    def calcula_densidade_usuarios(self):
        densidade_usarios = get_gompertz(TUM.CONFIG_DEFAULT.proporcao_final_usuario_internet,
                                         TUM.CONFIG_DEFAULT.inicio_adocao,
                                         TUM.CONFIG_DEFAULT.taxa_crescimento_usuarios_internet,
                                         self.tempo_analise)
        self.densidade_usuarios = densidade_usarios * self.densidade_demografica * self.percentual_pop_ativa

    def calcula_trafego_terminal(self):
        # Inicializa duas matrizes com 3 linhas (tipos de terminais) x 'tempo_analise' colunas
        r_j = np.zeros((3, self.tempo_analise))
        rs_j = np.zeros((3, self.tempo_analise))

        heavy_users = get_gompertz(TUM.CONFIG_DEFAULT.proporcao_final_terminais_heavy,
                                   TUM.CONFIG_DEFAULT.inicio_adocao,
                                   TUM.CONFIG_DEFAULT.taxa_crescimento_terminais_heavy,
                                   self.tempo_analise)

        # ela era um array e converteu ele em uma matriz de uma linha
        heavy_users = np.array([heavy_users])

        # ele cria uma matriz ordinary para receber o resultado da subtracao entre 1 e o primeiro, segundo...
        # elemento da matriz heavy e coloca o resultado na respectiva posicao da matriz ordinary
        ordinary_users = 1 - heavy_users

        self.user_fraction = np.concatenate((heavy_users, ordinary_users), axis=0)

        # Linhas: r_heavy/rordinary; Colunas: PC/Tablets/Smartphones
        # Valores expressos em Mbps
        # demanda_trafego_terminais = np.array([[0.125, 0.06244444, 0.01562222], [0.031, 0.00780556, 0.00195278]])
        demanda_trafego_terminais = np.array([[25.0, 7.0, 5.0], [3.125, 1.625, 1.25]])  # valores aumentados

        for i in range(self.tempo_analise):
            r_j[:, i] = np.asmatrix(self.user_fraction[:, i].T).dot(demanda_trafego_terminais)

        # Proporção entre terminais PC/Tablets/Smartphones
        # Valores: 20%/10%/70%
        s_j = np.array([[0.2, 0.1, 0.7]])

        # Multiplica ponto-a-ponto cada coluna de r_j por s_j
        for i in range(self.tempo_analise):
            rs_j[:, i] = np.multiply(r_j[:, i], s_j)

        self.demanda_trafego_terminais = np.sum(rs_j,
                                                 axis=0)  # achata somando as linhas, resultado em 1 linha e 15 colunas

    def calcula_demada_usuarios(self):
        self.demanda_usuarios = self.densidade_usuarios * TUM.CONFIG_DEFAULT.taxa_usuarios_ativos \
                                 * self.demanda_trafego_terminais

    def calcula_demanda_trafego(self):
        self.calcula_demanda_aplicacoes()
        self.calcula_densidade_usuarios()
        self.calcula_trafego_terminal()
        self.calcula_demada_usuarios()
        self.demanda_trafego = np.add(self.demanda_aplicacoes, self.demanda_usuarios)  # faco um chuveirinho somando

    def __capacidade_atendimento_rede_acesso(self):
        capacidade_atendimento_macro = 0.0
        capacidade_atendimento_femto = 0.0
        for c in self.lista_bs['implantacao_macro']:
            capacidade_atendimento_macro += (c.tipo_BS.capacidade * c.tipo_BS.setores)
        for c in self.lista_bs['implantacao_femto']:
            capacidade_atendimento_femto += (c.tipo_BS.capacidade * c.tipo_BS.setores)
        return capacidade_atendimento_macro, capacidade_atendimento_femto

    def __checa_possui_bs_atualizavel(self, ano, tipo):
        result = False
        if tipo == 'Macro':
            for bs in self.lista_bs['implantacao_macro']:
                if ano <= self.tempo_maturacao and bs.tipo_BS.tecnologia == '4G':
                    continue
                result = result or bs.tipo_BS.atualizavel
        else:
            for bs in self.lista_bs['implantacao_femto']:
                if ano <= self.tempo_maturacao and bs.tipo_BS.tecnologia == '4G':
                    continue
                result = result or bs.tipo_BS.atualizavel
        return result

    def __upgrade_bs(self, t, demanda_expansao, tipo):
        if demanda_expansao >=0:
            if tipo == 'Macro':
                lista_bs = self.lista_bs['implantacao_macro']
            else:
                lista_bs = self.lista_bs['implantacao_femto']

            capacidade_expandida_acumulada = 0.0
            for bs in lista_bs:
                if t <= self.tempo_maturacao and bs.tipo_BS.tecnologia == '4G':
                    print('Período de maturação tecnológica. BS não será atualizada para 5G.')
                    continue
                capacidade_antes = bs.tipo_BS.capacidade * bs.tipo_BS.setores
                print('Capacidade antes da Atualização: {} Mbps ({} BS com tecnologia {})'.format(capacidade_antes,
                                                                                               bs.tipo_BS.tipo,
                                                                                                   bs.tipo_BS.tecnologia))
                bs.upgrade()
                capacidade_depois = bs.tipo_BS.capacidade * bs.tipo_BS.setores
                print('Capacidade após Atualização: {} Mbps ({} BS com tecnologia {})'.format(capacidade_depois,
                                                                                              bs.tipo_BS.tipo,
                                                                                               bs.tipo_BS.tecnologia))
                capacidade_expandida_acumulada += (capacidade_depois - capacidade_antes)
                if capacidade_expandida_acumulada > demanda_expansao:
                    break

    def __implatacao_novas_bs(self, t, demanda_expansao, tipo_bs):
        if tipo_bs == 'Macro':
            if t <= self.tempo_maturacao:
                tipo = BSType.MACRO_4G
            else:
                tipo = BSType.MACRO_5G
        else:
            if t <= self.tempo_maturacao:
                tipo = BSType.FEMTO_4G
            else:
                tipo = BSType.FEMTO_5G

        print('Inclusão de BSs por Capacidade em {} Mbps'.format(demanda_expansao))
        n_bs = np.ceil( demanda_expansao/ (tipo.capacidade * tipo.setores) )
        print('Implantar {} BSs com tecnologia {}'.format(n_bs, tipo.tecnologia))
        for nb in range(int(n_bs)):
            nova_bs = BS(0, tipo, False)
            if tipo_bs == 'Macro':
                self.lista_bs['implantacao_macro'].append(nova_bs)
            else:
                self.lista_bs['implantacao_femto'].append(nova_bs)

    def calcula_dimensionamento_rede_acesso(self):
        print('Dimensionamento da Rede de Rádio do Aglomerado {}:'.format(self.id))
        for ano, demanda_ano in enumerate(self.demanda_trafego):
            demanda = demanda_ano * self.area_aglomerado
            print('Ano (t): {}'.format(ano))
            print('Demanda de Trafego: {} Mbps'.format(demanda))

            capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
            print('Estratégia de Implantação Macro:')
            print('Capacidade de Atendimento de BSs existentes: {} Mbps'.format(capacidade_atendimento_macro))
            print('Estratégia de Implantação Femto:')
            print('Capacidade de Atendimento de BSs existentes: {} Mbps'.format(capacidade_atendimento_femto))
            print()

            demanda_expansao_macro = demanda - capacidade_atendimento_macro
            demanda_expansao_femto = demanda - capacidade_atendimento_femto

            if demanda_expansao_macro >= 0 or demanda_expansao_femto >= 0:
                if demanda_expansao_macro >= 0:
                    print('Estratégia de Implantação Macro')
                    print('Necessidade de atualização em {} Mbps'.format(demanda_expansao_macro))

                if demanda_expansao_femto >= 0:
                    print('Estratégia de Implantação Femto')
                    print('Necessidade de atualização em {} Mbps'.format(demanda_expansao_femto))

                print()

                teste_condicao = self.__checa_possui_bs_atualizavel(ano, 'Macro')
                print('É possível o upgrade de BSs na Estratégia de Implantação Macro Only? {}'.format(teste_condicao))

                if teste_condicao is True:
                    print('Executa atualizacoes de Macro BSs')
                    self.__upgrade_bs(ano, demanda_expansao_macro, 'Macro')
                print()

                teste_condicao = self.__checa_possui_bs_atualizavel(ano, 'Femto')
                print('É possível o upgrade de BSs na Estratégia de Implantação Femto? {}'.format(teste_condicao))
                if teste_condicao is True:
                    print('Executa atualizacoes de Femto BSs')
                    self.__upgrade_bs(ano, demanda_expansao_femto, 'Femto')
                print()

                capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
                demanda_expansao_macro = demanda - capacidade_atendimento_macro
                demanda_expansao_femto = demanda - capacidade_atendimento_femto

                if demanda_expansao_macro >= 0:
                    print('Estratégia de Implantação Macro Only: Necessidade de implantação de novas BSs')
                    print('Realiza a implantação de BSs novas do tipo Macro')
                    self.__implatacao_novas_bs(ano, demanda_expansao_macro, 'Macro')
                    print()
                if demanda_expansao_femto >= 0:
                    print('Estratégia de Implantação Femto: Necessidade de implantação de novas BSs')
                    print('Realiza a implantação de BSs novas do tipo Femto')
                    self.__implatacao_novas_bs(ano, demanda_expansao_femto, 'Femto')
                    print()
            else:
                print('Rede de Acesso não precisa ser atualizada')
            print()
