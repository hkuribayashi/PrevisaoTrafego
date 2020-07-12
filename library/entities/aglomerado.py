import numpy as np
import copy as cp

from library.entities.aplicacacao import Aplicacao
from library.hetnet.trafego_usuarios import TrafegoUsuariosMoveis as TUM
from library.hetnet.tipo_bs import TipoBS
from library.hetnet.bs import BS
from library.util.util import get_gompertz, get_ponto_aleatorio, busca_bs_nao_hub, get_distancia_manhattan, busca_bs_hub


# noinspection PyUnresolvedReferences
class Aglomerado:

    def __init__(self, id_, total_habitantes, area_aglomerado, total_agencias_bancarias, total_domicilios,
                 total_cruzamentos, tipo_aglomerado,
                 tipo_cenario='Original',
                 cenario_original=-1,
                 estrategia_atualizacao_bs='Tradicional'):

        self.id = id_
        self.total_habitantes = total_habitantes
        self.area_aglomerado = area_aglomerado
        self.total_agencias_bancarias = total_agencias_bancarias
        self.total_domicilios = total_domicilios
        self.densidade_demografica = total_habitantes/area_aglomerado

        self.total_cruzamentos = total_cruzamentos
        self.tipo_aglomerado = tipo_aglomerado
        self.tipo_cenario = tipo_cenario
        self.cenario_original = cenario_original
        self.estrategia_atualizacao_bs = estrategia_atualizacao_bs

        self.total_servidores_publicos = 0.0
        self.total_servidores_publicos_saude = 0.0
        self.total_trabalhadores_informais = 0.0
        self.total_alunos = 0.0
        self.total_docentes = 0.0
        self.total_veiculos = 0.0
        self.tempo_analise = 0
        self.percentual_alunos_ead = 0.0
        self.percentual_pop_ativa = 0.0
        self.total_pop_ativa = 0.0
        self.total_pop_inativa = 0.0

        self.percentual_habitantes = 0.0
        self.demanda_trafego_por_area = 0.0
        self.demanda_trafego = 0.0
        self.densidade_usuarios = 0.0
        self.demanda_trafego_terminais = 0.0
        self.demanda_usuarios = 0.0
        self.demanda_aplicacoes = 0.0
        self.user_fraction = 0.0
        self.tempo_maturacao = 3.0
        self.lista_bs = dict(implantacao_macro=list(), implantacao_hetnet=list())
        self.capacidade_atendimento_rede_acesso = dict(implantacao_macro=list(), implantacao_hetnet=list())
        self.quantidade_bs = dict(implantacao_macro=list(), implantacao_hetnet=list())

        # Equipamentos Fibra (PON)
        self.qtd_fibra_instalada_macro_only = 0.0
        self.qtd_modem_pon_macro_only = 0.0
        self.qtd_fibra_instalada_hetnet = 0.0
        self.qtd_modem_pon_hetnet = 0.0

        # Equipamentos MicroWave (MW)
        self.qtd_antena_mw_pt_pt_macro_only = 0.0
        self.qtd_sw_carrier_mw_macro_only = 0.0
        self.qtd_antena_mw_pt_pt_hetnet = 0.0
        self.qtd_sw_carrier_mw_hetnet = 0.0

        # Despesas de CAPEX de Radio
        self.capex_radio_macro = 0.0
        self.capex_radio_hetnet = 0.0

        # Despesas de OPEX de Radio
        self.opex_radio_macro = 0.0
        self.opex_radio_hetnet = 0.0

        if self.tipo_cenario == 'Alternativo' and self.cenario_original == -1:
            raise RuntimeError('Erro: Deve ser informado o aglomerado original')

    def adicionar_BS(self, BS):
        self.lista_bs['implantacao_macro'].append(BS)
        self.lista_bs['implantacao_hetnet'].append(cp.deepcopy(BS))

    def calcula_demanda_aplicacoes(self):
        demanda_aplicacoes = np.zeros(self.tempo_analise)
        print('Dados de Aplicações de IoT/M2M para o Aglomerado {} ({}+{})'.format(self.id, self.tipo_cenario, self.estrategia_atualizacao_bs))
        for app in Aplicacao:
            qtd_terminais = 0.0
            if app.id == 1:
                qtd_terminais = self.total_habitantes
            else:
                if app.id == 2:
                    qtd_terminais = np.ceil(self.total_habitantes / 1000.0)
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
                                            if app.id == 9:
                                                qtd_terminais = np.ceil(self.total_pop_ativa -
                                                                        self.total_servidores_publicos -
                                                                        self.total_servidores_publicos_saude)
                                            else:
                                                if app.id == 10 or app.id == 11:
                                                    qtd_terminais = self.total_domicilios
                                                else:
                                                    qtd_terminais = np.ceil(self.total_veiculos)
            c = get_gompertz(app.mu, app.beta, app.gamma, self.tempo_analise)
            c = (qtd_terminais / self.area_aglomerado) * app.alpha * c * app.vazao
            print('Aplicação IoT: {} (alpha={}, beta={}, mu={}, gamma={}, terminais={}, vazao={})'.format(app.nome,
                                                                                                          app.alpha,
                                                                                                          app.beta,
                                                                                                          app.mu,
                                                                                                          app.gamma,
                                                                                                          qtd_terminais,
                                                                                                          app.vazao))
            demanda_aplicacoes += c
        self.demanda_aplicacoes = demanda_aplicacoes
        print()

    def calcula_densidade_usuarios(self):
        densidade_usuarios = get_gompertz(TUM.CONFIG_DEFAULT.proporcao_final_usuario_internet,
                                          TUM.CONFIG_DEFAULT.inicio_adocao,
                                          TUM.CONFIG_DEFAULT.taxa_crescimento_usuarios_internet,
                                          self.tempo_analise)
        self.densidade_usuarios = densidade_usuarios * self.densidade_demografica * self.percentual_pop_ativa

    def calcula_trafego_terminal(self):
        # Inicializa duas matrizes com 3 linhas (tipos de terminais) x 15 colunas (tempo_analise)
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
        self.demanda_trafego_por_area = np.add(self.demanda_aplicacoes,
                                               self.demanda_usuarios)  # faco um chuveirinho somando

    def __capacidade_atendimento_rede_acesso(self):
        capacidade_atendimento_macro = 0.0
        capacidade_atendimento_femto = 0.0
        for c in self.lista_bs['implantacao_macro']:
            capacidade_atendimento_macro += (c.tipo_BS.capacidade * c.tipo_BS.setores)
        for c in self.lista_bs['implantacao_hetnet']:
            capacidade_atendimento_femto += (c.tipo_BS.capacidade * c.tipo_BS.setores)
        return capacidade_atendimento_macro, capacidade_atendimento_femto

    def __checa_possui_bs_atualizavel(self, ano, tipo):
        result = False
        if tipo == 'Macro':
            for bs in self.lista_bs['implantacao_macro']:
                result = result or bs.tipo_BS.atualizavel
        else:
            for bs in self.lista_bs['implantacao_hetnet']:
                result = result or bs.tipo_BS.atualizavel
        return result

    def __upgrade_bs(self, t, demanda_expansao, tipo):
        if demanda_expansao >= 0:
            if tipo == 'Macro':
                lista_bs = self.lista_bs['implantacao_macro']
            else:
                lista_bs = self.lista_bs['implantacao_hetnet']

            capacidade_expandida_acumulada = 0.0
            for bs in lista_bs:
                capacidade_antes = bs.tipo_BS.capacidade * bs.tipo_BS.setores
                print('Capacidade antes da Atualização: {} Mbps ({} BS com tecnologia {})'.format(capacidade_antes,
                                                                                                  bs.tipo_BS.tipo,
                                                                                                  bs.tipo_BS.tecnologia))
                if self.estrategia_atualizacao_bs == 'Tradicional':
                    bs.upgrade(t)
                elif self.estrategia_atualizacao_bs == 'Acelerada':
                    bs.upgrade_5G(t)
                else:
                    raise RuntimeError('Estratégia de Atualização de BS não encontrada: {}'.format(self.estrategia_atualizacao_bs))

                capacidade_depois = bs.tipo_BS.capacidade * bs.tipo_BS.setores
                print('Capacidade após Atualização: {} Mbps ({} BS com tecnologia {})'.format(capacidade_depois,
                                                                                              bs.tipo_BS.tipo,
                                                                                              bs.tipo_BS.tecnologia))
                capacidade_expandida_acumulada += (capacidade_depois - capacidade_antes)
                if capacidade_expandida_acumulada > demanda_expansao:
                    break

    def __implatacao_novas_bs(self, t, demanda_expansao, tipo_bs):
        if tipo_bs == 'Macro':
            if self.estrategia_atualizacao_bs == 'Tradicional':
                if t <= self.tempo_maturacao:
                    tipo = TipoBS.MACRO_45G
                else:
                    tipo = TipoBS.MACRO_5G
            elif self.estrategia_atualizacao_bs == 'Acelerada':
                tipo = TipoBS.MACRO_5G
            else:
                raise RuntimeError('Estratégia de Atualização de BS não encontrada: {}'.format(self.estrategia_atualizacao_bs))
        else:
            if self.estrategia_atualizacao_bs == 'Tradicional':
                if t <= self.tempo_maturacao:
                    tipo = TipoBS.FEMTO_45G
                else:
                    tipo = TipoBS.FEMTO_5G
            elif self.estrategia_atualizacao_bs == 'Acelerada':
                tipo = TipoBS.FEMTO_5G
            else:
                raise RuntimeError('Estratégia de Atualização de BS não encontrada: {}'.format(self.estrategia_atualizacao_bs))

        print('Inclusão de BSs por Capacidade em {} Mbps'.format(demanda_expansao))
        n_bs = np.ceil(demanda_expansao / (tipo.capacidade * tipo.setores))
        print('Implantar {} BSs com tecnologia {}'.format(n_bs, tipo.tecnologia))
        for nb in range(int(n_bs)):
            ponto = get_ponto_aleatorio()
            nova_bs = BS(0, tipo, ponto, t, False, False)
            if tipo_bs == 'Macro':
                self.lista_bs['implantacao_macro'].append(nova_bs)
            else:
                self.lista_bs['implantacao_hetnet'].append(nova_bs)

    def implanta_cobertura_basica(self, ano):
        ponto = get_ponto_aleatorio()
        if self.estrategia_atualizacao_bs == 'Tradicional':
            diff_macro = (TipoBS.MACRO_4G.cobertura_por_setor * TipoBS.MACRO_4G.setores) - self.area_aglomerado
            diff_micro = (TipoBS.MICRO_4G.cobertura_por_setor * TipoBS.MICRO_4G.setores) - self.area_aglomerado
            if diff_macro >= 0 and diff_micro >= 0:
                if diff_macro < diff_micro:
                    nova_bs = BS(0, TipoBS.MACRO_4G, ponto, ano, True, False)
                else:
                    nova_bs = BS(0, TipoBS.MICRO_4G, ponto, ano, True, False)
            else:
                nova_bs = BS(0, TipoBS.MACRO_4G, ponto, ano, True, False)

            print('Estratégia de Implantação Macro Only:')
            print('Implantação de uma Macro BS com tecnologia 4G')
            print('Estratégia de Implantação HetNet:')
            print('Implantação de uma {} BS com tecnologia {}'.format(nova_bs.tipo_BS.tipo, nova_bs.tipo_BS.tecnologia))

            self.lista_bs['implantacao_macro'].append(BS(0, TipoBS.MACRO_4G, ponto, ano, True, False))
            self.lista_bs['implantacao_hetnet'].append(nova_bs)

        elif self.estrategia_atualizacao_bs == 'Acelerada':
            diff_macro = (TipoBS.MACRO_5G.cobertura_por_setor * TipoBS.MACRO_5G.setores) - self.area_aglomerado
            diff_micro = (TipoBS.MICRO_5G.cobertura_por_setor * TipoBS.MICRO_5G.setores) - self.area_aglomerado
            if diff_macro >= 0 and diff_micro >= 0:
                if diff_macro < diff_micro:
                    nova_bs = BS(0, TipoBS.MACRO_5G, ponto, ano, True, False)
                else:
                    nova_bs = BS(0, TipoBS.MICRO_5G, ponto, ano, True, False)
            else:
                nova_bs = BS(0, TipoBS.MACRO_5G, ponto, ano, True, False)

            self.lista_bs['implantacao_macro'].append(BS(0, TipoBS.MACRO_5G, ponto, ano, True, False))
            self.lista_bs['implantacao_hetnet'].append(nova_bs)

            print('Estratégia de Implantação Macro Only:')
            print('Implantação de uma Macro BS com tecnologia 5G')
            print('Estratégia de Implantação HetNet:')
            print('Implantação de uma {} BS com tecnologia {}'.format(nova_bs.tipo_BS.tipo, nova_bs.tipo_BS.tecnologia))
        else:
            raise RuntimeError('Estratégia de Atualização de BS não encontrada: {}'.format(self.estrategia_atualizacao_bs))

    def calcula_dimensionamento_rede_acesso(self):
        print('Dimensionamento da Rede de Rádio do Aglomerado {} ({}+{}):'.format(self.id, self.tipo_cenario, self.estrategia_atualizacao_bs))
        for ano, demanda_ano in enumerate(self.demanda_trafego_por_area):
            self.demanda_trafego[ano] = demanda_ano * self.area_aglomerado
            print('Ano (t): {}'.format(ano))
            print('Demanda de Trafego: {} Mbps'.format(self.demanda_trafego[ano]))

            capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
            if capacidade_atendimento_macro == 0:
                print('Capacidade de Atendimento Inexistente no Aglomerado {}.'.format(self.id))
                print('Realizando a implantação de uma BS para criação de cobertura básica:')
                self.implanta_cobertura_basica(ano)
                print()

            capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
            self.capacidade_atendimento_rede_acesso['implantacao_macro'][ano] = capacidade_atendimento_macro
            self.capacidade_atendimento_rede_acesso['implantacao_hetnet'][ano] = capacidade_atendimento_femto

            print('Estratégia de Implantação Macro Only:')
            print('Capacidade de Atendimento de BSs existentes: {} Mbps'.format(capacidade_atendimento_macro))
            print('Estratégia de Implantação HetNet:')
            print('Capacidade de Atendimento de BSs existentes: {} Mbps'.format(capacidade_atendimento_femto))
            print()

            demanda_expansao_macro = self.demanda_trafego[ano] - capacidade_atendimento_macro
            demanda_expansao_femto = self.demanda_trafego[ano] - capacidade_atendimento_femto

            if demanda_expansao_macro >= 0 or demanda_expansao_femto >= 0:
                if demanda_expansao_macro >= 0:
                    print('Estratégia de Implantação Macro Only:')
                    print('Necessidade de atualização em {} Mbps'.format(demanda_expansao_macro))

                if demanda_expansao_femto >= 0:
                    print('Estratégia de Implantação HetNet:')
                    print('Necessidade de atualização em {} Mbps'.format(demanda_expansao_femto))

                print()

                teste_condicao = True
                while teste_condicao:
                    teste_condicao = self.__checa_possui_bs_atualizavel(ano, 'Macro')
                    print('É possível o upgrade de BSs na Estratégia de Implantação Macro Only? {}'.format(
                        teste_condicao))

                    if teste_condicao is True:
                        print('Executa atualizacoes de Macro BSs')
                        self.__upgrade_bs(ano, demanda_expansao_macro, 'Macro')
                    print()

                    capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
                    if self.demanda_trafego[ano] - capacidade_atendimento_macro <= 0:
                        break

                teste_condicao = True
                while teste_condicao:
                    teste_condicao = self.__checa_possui_bs_atualizavel(ano, 'HetNet')
                    print('É possível o upgrade de BSs na Estratégia de Implantação HetNet? {}'.format(teste_condicao))

                    if teste_condicao is True:
                        print('Executa atualizacoes de Femto BSs')
                        self.__upgrade_bs(ano, demanda_expansao_femto, 'Femto')
                    print()

                    capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
                    if self.demanda_trafego[ano] - capacidade_atendimento_femto <= 0:
                        break

                capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
                demanda_expansao_macro = self.demanda_trafego[ano] - capacidade_atendimento_macro
                demanda_expansao_femto = self.demanda_trafego[ano] - capacidade_atendimento_femto

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
            capacidade_atendimento_macro, capacidade_atendimento_femto = self.__capacidade_atendimento_rede_acesso()
            self.capacidade_atendimento_rede_acesso['implantacao_macro'][ano] = capacidade_atendimento_macro
            self.capacidade_atendimento_rede_acesso['implantacao_hetnet'][ano] = capacidade_atendimento_femto

    def _calcula_dimensionamento_rede_transporte_fibra(self, lista_bs):
        print('Implantação Fibra Aglomerado {}:'.format(self.id))
        total_bs = np.zeros(self.tempo_analise)
        quantidadade_fibra_instalada = np.zeros(self.tempo_analise)
        quantidade_modem_pon = np.zeros(self.tempo_analise)

        # Calcula a quantidade acumulada de BSs por ano
        for bs in lista_bs:
            for ano in range(bs.ano, self.tempo_analise):
                total_bs[ano] += 1

        print('Total Acumulado de BSs por Ano: ')
        print(total_bs)

        # Calcula as implantaçãoes de de fibra (km) e modems PON por ano
        max_numero_bs = -99.0
        for ano, total_ano in enumerate(total_bs):
            if total_ano > max_numero_bs:
                if total_ano == 1:
                    quantidadade_fibra_instalada[ano] = 0
                    quantidade_modem_pon[ano] = 1
                    max_numero_bs = total_ano
                else:
                    max_numero_bs = total_ano
                    hub = busca_bs_hub(lista_bs)  # nesse caso é a BS principal, agregadora de tráfego
                    quantidade_modem_pon[ano] = total_ano - np.sum(quantidade_modem_pon[:ano])
                    bs_nao_hub = busca_bs_nao_hub(lista_bs, ano)
                    for bs in bs_nao_hub:
                        quantidadade_fibra_instalada[ano] += get_distancia_manhattan(bs,
                                                                                    hub)  # a distancia esta em metros
        print('Quantidade de Fibra Instalada por Ano')
        print(quantidadade_fibra_instalada)

        print('Quantidade de Modem PON por Ano')
        print(quantidade_modem_pon)
        print()

        return quantidadade_fibra_instalada, quantidade_modem_pon

    def _calcula_dimensionamento_rede_transporte_microondas(self, lista_bs):
        print('Implantação Microwave Aglomerado {}:'.format(self.id))
        total_bs = np.zeros(self.tempo_analise)
        quantidade_antena_mw_pt_pt = np.zeros(self.tempo_analise)
        quantidade_sw_carrier_mw = np.zeros(self.tempo_analise)

        # Quantidade de portas por Switch
        quantidade_portas_sw_carrier = 12

        # Calcula a quantidade acumulada de BSs por ano
        for bs in lista_bs:
            for ano in range(bs.ano, self.tempo_analise):
                total_bs[ano] += 1

        print('Total Acumulado de BSs por Ano: ')
        print(total_bs)

        # Calcula as implantaçãoes de Antenas microondas
        max_numero_bs = -99.0
        for ano, total_ano in enumerate(total_bs):
            if total_ano > max_numero_bs:
                if total_ano == 1:
                    quantidade_antena_mw_pt_pt[ano] = 0
                    max_numero_bs = total_ano
                else:
                    max_numero_bs = total_ano
                    # Nesse caso, dentro do aglomerado chama-se a BS que não é Hub de ponto a ponto;
                    quantidade_antena_mw_pt_pt[ano] = total_ano - np.sum(quantidade_antena_mw_pt_pt[:ano]) - 1
            if np.sum(quantidade_sw_carrier_mw[:ano]) * quantidade_portas_sw_carrier < total_ano:
                quantidade_sw_carrier_mw[ano] = np.ceil(total_ano / quantidade_portas_sw_carrier) - \
                                                np.sum(quantidade_sw_carrier_mw[:ano])

        # Multiplico por 02 (dois) a quantidade de antennas pt-pt, pois é um par, para cada BS
        quantidade_antena_mw_pt_pt = quantidade_antena_mw_pt_pt * 2

        print('Total de Antenas MW Pt-Pt Implantadas por Ano:')
        print(quantidade_antena_mw_pt_pt)

        print('Total de SW Carrier Implantados por Ano:')
        print(quantidade_sw_carrier_mw)
        print()

        return quantidade_antena_mw_pt_pt, quantidade_sw_carrier_mw

    def calcula_dimensionamento_rede_transporte(self):
        print('Estratégia Macro:')
        self.qtd_fibra_instalada_macro_only, self.qtd_modem_pon_macro_only = \
            self._calcula_dimensionamento_rede_transporte_fibra(self.lista_bs['implantacao_macro'])

        print('Estratégia Hetnet:')
        self.qtd_fibra_instalada_hetnet, self.qtd_modem_pon_hetnet = \
            self._calcula_dimensionamento_rede_transporte_fibra(self.lista_bs['implantacao_hetnet'])

        print('Estratégia Macro:')
        self.qtd_antena_mw_pt_pt_macro_only, self.qtd_sw_carrier_mw_macro_only = \
            self._calcula_dimensionamento_rede_transporte_microondas(self.lista_bs['implantacao_macro'])

        print('Estratégia Hetnet:')
        self.qtd_antena_mw_pt_pt_hetnet, self.qtd_sw_carrier_mw_hetnet = \
            self._calcula_dimensionamento_rede_transporte_microondas(self.lista_bs['implantacao_hetnet'])
