import numpy as np
import matplotlib.pyplot as plt

from library.entities.Aplicacacao import AplicacaoFaroSede
from library.hetnet.TrafegoUsuariosMoveis import TrafegoUsuariosMoveis as TUM
from library.hetnet.BSType import BSType
from library.hetnet.BS import BS
from library.util.Util import get_gompertz


class Aglomerado:

    def __init__(self, id_, total_habitantes, area_aglomerado, total_agencias_bancarias, total_domicilios,
                 percentual_populacao_ativa):
        self._id = id_
        self._total_habitantes = total_habitantes
        self._area_aglomerado = area_aglomerado
        self._total_agencias_bancarias = total_agencias_bancarias
        self._total_domicilios = total_domicilios
        self._densidade_demografica = total_habitantes/area_aglomerado
        self._percentual_populacao_ativa = percentual_populacao_ativa
        self._total_pop_ativa = self._percentual_populacao_ativa * self._total_habitantes
        self._total_pop_inativa = self._total_habitantes - self._total_pop_ativa

        self._total_servidores_publicos = 0.0
        self._total_servidores_publicos_saude = 0.0
        self._total_trabalhadores_informais = 0.0
        self._total_veiculos = 0.0
        self._tempo_analise = 0

        self._percentual_habitantes = 0.0
        self._demanda_trafego = 0.0
        self._densidade_usuarios = 0.0
        self._demanda_trafego_terminais = 0.0
        self._demanda_usuarios = 0.0
        self._demanda_aplicacoes = 0.0
        self._user_fraction = 0.0
        self._lista_bs = list()

    @property
    def total_habitantes(self):
        return self._total_habitantes

    @property
    def total_pop_ativa(self):
        return self._total_pop_ativa



    def adicionar_BS(self, BS):
        self._lista_bs.append(BS)

    def calcula_demanda_aplicacoes(self):
        demanda_aplicacoes = np.zeros(self._tempo_analise)
        for app in AplicacaoFaroSede:
            c = get_gompertz(app.mu, app.beta, app.gamma, self._tempo_analise)
            c = (app.qtd_terminais / self._area_aglomerado) * app.alpha * c
            demanda_aplicacoes += c
        self._demanda_aplicacoes = demanda_aplicacoes

    def calcula_densidade_usuarios(self):
        densidade_usarios = get_gompertz(TUM.CONFIG_DEFAULT.proporcao_final_usuario_internet,
                                         TUM.CONFIG_DEFAULT.inicio_adocao,
                                         TUM.CONFIG_DEFAULT.taxa_crescimento_usuarios_internet,
                                         self._tempo_analise)
        self._densidade_usuarios = densidade_usarios * self._densidade_demografica * self._percentual_populacao_ativa

    def calcula_trafego_terminal(self):
        # Inicializa duas matrizes com 3 linhas (tipos de terminais) x 'tempo_analise' colunas
        r_j = np.zeros((3, self._tempo_analise))
        rs_j = np.zeros((3, self._tempo_analise))

        heavy_users = get_gompertz(TUM.CONFIG_DEFAULT.proporcao_final_terminais_heavy,
                                   TUM.CONFIG_DEFAULT.inicio_adocao,
                                   TUM.CONFIG_DEFAULT.taxa_crescimento_terminais_heavy,
                                   self._tempo_analise)

        # ela era um array e converteu ele em uma matriz de uma linha
        heavy_users = np.array([heavy_users])

        # ele cria uma matriz ordinary para receber o resultado da subtracao entre 1 e o primeiro, segundo...
        # elemento da matriz heavy e coloca o resultado na respectiva posicao da matriz ordinary
        ordinary_users = 1 - heavy_users

        self._user_fraction = np.concatenate((heavy_users, ordinary_users), axis=0)

        # Linhas: r_heavy/rordinary; Colunas: PC/Tablets/Smartphones
        # Valores expressos em Mbps
        # demanda_trafego_terminais = np.array([[0.125, 0.06244444, 0.01562222], [0.031, 0.00780556, 0.00195278]])
        demanda_trafego_terminais = np.array([[25.0, 5.0, 2.0], [3.125, 0.625, 0.25]])  # valores aumentados

        for i in range(self._tempo_analise):
            r_j[:, i] = np.asmatrix(self._user_fraction[:, i].T).dot(demanda_trafego_terminais)

        # Proporção entre terminais PC/Tablets/Smartphones
        # Valores: 20%/10%/70%
        s_j = np.array([[0.2, 0.1, 0.7]])

        # Multiplica ponto-a-ponto cada coluna de r_j por s_j
        for i in range(self._tempo_analise):
            rs_j[:, i] = np.multiply(r_j[:, i], s_j)

        self._demanda_trafego_terminais = np.sum(rs_j,
                                                 axis=0)  # achata somando as linhas, resultado em 1 linha e 15 colunas

    def calcula_demada_usuarios(self):
        self._demanda_usuarios = self._densidade_usuarios * TUM.CONFIG_DEFAULT.taxa_usuarios_ativos \
                                 * self._demanda_trafego_terminais

    def calcula_demanda_trafego(self):
        self.calcula_demanda_aplicacoes()
        self.calcula_densidade_usuarios()
        self.calcula_trafego_terminal()
        self.calcula_demada_usuarios()
        self._demanda_trafego = np.add(self._demanda_aplicacoes, self._demanda_usuarios)  # faco um chuveirinho somando

    def capacidade_rede_acesso(self):
        capacidade_atendimento = 0.0
        for c in self._lista_bs:
            capacidade_atendimento += (c.tipo_BS.capacidade * c.tipo_BS.setores)
        return capacidade_atendimento

    def checa_possui_bs_atualizavel(self, t):
        result = False
        for b in self._lista_bs:
            if t <= 3 and b.tipo_BS.tecnologia == '4G':
                continue
            result = result or b.tipo_BS.atualizavel
        return result

    def upgrade_bs(self, t, capacidade_expansao):
        capacidade_expandida_acumulada = 0.0
        for b in self._lista_bs:
            capacidade_antes = b.tipo_BS.capacidade * b.tipo_BS.setores
            print('Capacidade antes da Atualização: {} Mbps (BS com tecnologia {})'.format(capacidade_antes,
                                                                                           b.tipo_BS.tecnologia))
            if t <= 3 and b.tipo_BS.tecnologia == '4G':
                continue
            b.upgrade()
            capacidade_depois = b.tipo_BS.capacidade * b.tipo_BS.setores
            print('Capacidade após Atualização: {} Mbps (BS com tecnologia {})'.format(capacidade_depois,
                                                                                       b.tipo_BS.tecnologia))
            capacidade_expandida_acumulada += (capacidade_depois - capacidade_antes)
            if (capacidade_expandida_acumulada > capacidade_expansao):
                break

    def implatacao_novas_bs(self, t, capacidade_expansao):
        cobertura_existente = 0.0
        for b in self._lista_bs:
            cobertura_existente += b.tipo_BS.cobertura
        area_descoberta = self._area_aglomerado - cobertura_existente
        if area_descoberta >= 0:
            print('Existência de área a ser coberta')
            print('Inclusão de BSs por Cobertura')
            n_BS_macro = area_descoberta / BSType.MACRO_4G.cobertura
            print('Necessário implantar {} BSs'.format(n_BS_macro))
            n_BS_femto = area_descoberta / BSType.FEMTO_4G.cobertura
            print('Necessário implantar {} BSs'.format(n_BS_femto))
        else:
            print('Area já totalmente coberta')
            print('Necessária inclusão de BSs por Capacidade em {} Mbps'.format(capacidade_expansao))
            print('Estratégia 1: Macro BS only')
            if t <= 3:
                n_BS_macro = np.ceil(capacidade_expansao / (BSType.MACRO_4G.capacidade * BSType.MACRO_4G.setores))
                print('Implantar {} BSs com tecnologia {}'.format(n_BS_macro, BSType.MACRO_4G.tecnologia))
                for nb in range(int(n_BS_macro)):
                    nova_bs = BS(BSType.MACRO_4G, False)
                    self._lista_bs.append(nova_bs)
            else:
                n_BS_macro = np.ceil(capacidade_expansao / (BSType.MACRO_5G.capacidade * BSType.MACRO_5G.setores))
                print('Implantar {} BSs com tecnologia {}'.format(n_BS_macro, BSType.MACRO_5G.tecnologia))
                for nb in range(int(n_BS_macro)):
                    nova_bs = BS(BSType.MACRO_4G, False)
                    self._lista_bs.append(nova_bs)

    def calcula_dimensionamento_rede_acesso(self):
        for indx, dt in enumerate(self._demanda_trafego):
            demanda = dt * self._area_aglomerado
            print('Ano (t): {}'.format(indx))
            print('Demanda de Trafego: {} Mbps'.format(demanda))

            capacidade_atendimento = self.capacidade_rede_acesso()
            print('Capacidade de Atendimento: {} Mbps'.format(capacidade_atendimento))

            capacidade_expansao = demanda - capacidade_atendimento
            if capacidade_expansao >= 0:
                print('Atualização em {} Mbps'.format(capacidade_expansao))
                teste_condicao = self.checa_possui_bs_atualizavel(indx)
                print('É possível o upgrade de BSs ? {}'.format(teste_condicao))
                if teste_condicao is True:
                    print('Executa atualizacoes de BSs')
                    self.upgrade_bs(indx, capacidade_expansao)
                    capacidade_atendimento = self.capacidade_rede_acesso()
                    capacidade_expansao = demanda - capacidade_atendimento
                    if capacidade_expansao >= 0:
                        print('Realiza a implantação de BSs novas')
                        self.implatacao_novas_bs(indx, capacidade_expansao)
                else:
                    print('Realiza a implantação de BSs novas')
                    self.implatacao_novas_bs(indx, capacidade_expansao)
            else:
                print('Não precisa ser atualizado')
            print('\n')
