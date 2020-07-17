import numpy as np

from library.custos.capex import CAPEX
from library.custos.opex import OPEX
from library.util import util


class TcoTransporte:

    def __init__(self, municipio):
        self.municipio = municipio
        self.tipos_rede_radio = ['Macro', 'Hetnet']

        # Despesas de CAPEX de Transporte MW+Macro
        self.capex_transporte_mw_macro = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                              equipamentos=np.zeros(self.municipio.tempo_analise),
                                              instalacao=np.zeros(self.municipio.tempo_analise))

        # Despesas de OPEX de Transporte MW+MACRO
        self.opex_transporte_mw_macro = dict(energia=np.zeros(self.municipio.tempo_analise),
                                             manutencao=np.zeros(self.municipio.tempo_analise),
                                             aluguel=np.zeros(self.municipio.tempo_analise),
                                             falhas=np.zeros(self.municipio.tempo_analise))

        # Despesas de CAPEX de Transporte MW+Hetnet
        self.capex_transporte_mw_hetnet = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                               equipamentos=np.zeros(self.municipio.tempo_analise),
                                               instalacao=np.zeros(self.municipio.tempo_analise))

        # Despesas de OPEX de Transporte MW+Hetnet
        self.opex_transporte_mw_hetnet = dict(energia=np.zeros(self.municipio.tempo_analise),
                                              manutencao=np.zeros(self.municipio.tempo_analise),
                                              aluguel=np.zeros(self.municipio.tempo_analise),
                                              falhas=np.zeros(self.municipio.tempo_analise))

    def get_tco(self):
        self.__calcula_capex_transporte()
        self.__calcula_opex_transporte()

    def __calcula_opex_transporte(self):
        for ag in self.municipio.aglomerados:
            print('OPEX de Transporte do Aglomerado {}:'.format(ag.id))
            for tipo in self.tipos_rede_radio:
                if tipo == 'Macro':
                    qtd_antena_mw= ag.qtd_antena_mw_pt_pt_macro_only
                    qtd_sw_carrier_mw = ag.qtd_sw_carrier_mw_macro_only
                    aglomerado  = ag.opex_transporte_mw_macro
                    tco_transporte = self.opex_transporte_mw_macro
                else:
                    qtd_antena_mw = ag.qtd_antena_mw_pt_pt_hetnet
                    qtd_sw_carrier_mw = ag.qtd_sw_carrier_mw_hetnet
                    aglomerado = ag.opex_transporte_mw_hetnet
                    tco_transporte = self.opex_transporte_mw_hetnet

                energia = self.__calcula_opex_transporte_mw_energia(qtd_antena_mw, qtd_sw_carrier_mw)
                manutencao = self.__calcula_opex_transporte_mw_manutencao(qtd_antena_mw, qtd_sw_carrier_mw)
                aluguel = self.__calcula_opex_transporte_mw_aluguel(qtd_antena_mw)
                falhas = self.__calcula_opex_transporte_mw_falhas(qtd_antena_mw, qtd_sw_carrier_mw)

                aglomerado['energia'] += energia
                aglomerado['manutencao'] += manutencao
                aglomerado['aluguel'] += aluguel
                aglomerado['falhas'] += falhas

                if ag.tipo_cenario == 'Original':
                    tco_transporte['energia'] += energia
                    tco_transporte['manutencao'] += manutencao
                    tco_transporte['aluguel'] += aluguel
                    tco_transporte['falhas'] += falhas

                print('Implantação Transporte MW+{}:'.format(tipo))
                print('OPEX Transporte - Energia:')
                print(energia)
                print('OPEX Trasnporte - Manutenção:')
                print(manutencao)
                print('OPEX Transporte - Aluguel:')
                print(aluguel)
                print('OPEX Transporte - Falhas:')
                print(falhas)
                print()

    def __calcula_opex_transporte_mw_energia(self, qtd_antena_mw, qtd_sw_carrier_mw):
        energia = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula-se a variacao da tarifa de energia ao longo dos anos
        tarifa_energia_ajustada = util.atualizacao_linear(OPEX.CONSUMO.valor,
                                                          OPEX.TAXA_REAJUSTE.valor,
                                                          self.municipio.tempo_analise)

        # Computar consumo da Antena Large para todos os Anos do Tempo de Análise
        # Assumindo Potência 530W (Antena MW Large)
        consumo_mw_large = tarifa_energia_ajustada * 365.0 * 24 * (530.0 / 1000.0) * 2.0
        energia += consumo_mw_large

        for ano, qtd_antena in enumerate(qtd_antena_mw):
            if qtd_antena > 0 or qtd_sw_carrier_mw[ano] > 0:
                energia_mw = np.zeros(self.municipio.tempo_analise)
                qtd_sw = qtd_sw_carrier_mw[ano]
                for t in range(ano, self.municipio.tempo_analise):
                    # Faz o cálculo do volume de $ por kWh ao ano
                    # Assumindo Potência 100W (Antena MW Small) e 450W (SW Carrier)
                    energia_mw[t] += (100.0 / 1000.0) * \
                                      qtd_antena * \
                                      tarifa_energia_ajustada[t] * \
                                      365.0 * \
                                      24.0
                    energia_mw[t] += (450.0 / 1000.0) * \
                                      qtd_sw * \
                                      tarifa_energia_ajustada[t] * \
                                      365.0 * \
                                      24.0
                energia += energia_mw

        return energia

    def __calcula_opex_transporte_mw_manutencao(self, qtd_antena_mw, qtd_sw_carrier_mw):
        manutencao = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualizacao do valor de manutenção ajustado por ano
        manutencao_mw_large_ajustado = util.atualizacao_linear(OPEX.MANUTENCAO_MW_LARGE.valor,
                                                               OPEX.TAXA_REAJUSTE.valor,
                                                               self.municipio.tempo_analise)

        manutencao_mw_small_ajustado = util.atualizacao_linear(OPEX.MANUTENCAO_MW_SMALL.valor,
                                                               OPEX.TAXA_REAJUSTE.valor,
                                                               self.municipio.tempo_analise)

        manutencao_sw_ajustado = util.atualizacao_linear(OPEX.MANUTENCAO_SW.valor,
                                                         OPEX.TAXA_REAJUSTE.valor,
                                                         self.municipio.tempo_analise)

        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        despesas_rh = valor_salario_tecnico_ajustado * \
                      OPEX.QTD_TECNICOS.valor * \
                      OPEX.QTD_TIMES.valor * \
                      ((2.0 * self.municipio.tempo_viagem) + OPEX.MTTR_MW_LARGE.valor)

        manutencao += (manutencao_mw_large_ajustado + despesas_rh)

        for ano, qtd_antena in enumerate(qtd_antena_mw):
            manutencao_small = np.zeros(self.municipio.tempo_analise)
            if qtd_antena > 0 or qtd_sw_carrier_mw[ano]:
                for t in range(ano, self.municipio.tempo_analise):
                    # Custo de Manutenção do Equipamento de Hardware (MW)
                    manutencao_small[t] += manutencao_mw_small_ajustado[t]

                    # Custo de Manutenção do Equipamento de Hardware (SW)
                    manutencao_small[t] += manutencao_sw_ajustado[t] * qtd_sw_carrier_mw[t]

                    # Custo de Manutenção do Equipamento (RH)
                    manutencao_small[t] += valor_salario_tecnico_ajustado[t] * \
                                           OPEX.QTD_TECNICOS.valor * \
                                           OPEX.QTD_TIMES.valor * \
                                           ((OPEX.MTTR_MW_SMALL.valor * qtd_antena)  +
                                            (OPEX.MTTR_MW_SW.valor * qtd_sw_carrier_mw[t]))
            manutencao += manutencao_small

        return manutencao

    def __calcula_opex_transporte_mw_aluguel(self, qtd_antena_mw):
        aluguel = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula-se a variacao da tarifa de licenciamento ao longo dos anos
        tarifa_licenciamento_large_ajustada = util.atualizacao_linear(OPEX.LICENSA_MW_LARGE.valor,
                                                                      OPEX.TAXA_REAJUSTE.valor,
                                                                      self.municipio.tempo_analise)

        tarifa_licenciamento_small_ajustada = util.atualizacao_linear(OPEX.LICENSA_MW_SMALL.valor,
                                                                      OPEX.TAXA_REAJUSTE.valor,
                                                                      self.municipio.tempo_analise)
        aluguel += tarifa_licenciamento_large_ajustada

        for ano, qtd_antena in enumerate(qtd_antena_mw):
            if qtd_antena > 0:
                aluguel_espectro = np.zeros(self.municipio.tempo_analise)
                for t in range(ano, self.municipio.tempo_analise):
                    aluguel_espectro[t] += tarifa_licenciamento_small_ajustada[t]
                aluguel += aluguel_espectro

        return aluguel

    def __calcula_opex_transporte_mw_falhas(self, qtd_antena_mw, qtd_sw_carrier_mw):
        falhas = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        manutencao_hardware_mw_small = util.atualizacao_linear(OPEX.MANUTENCAO_MW_SMALL.valor,
                                                               OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                               self.municipio.tempo_analise)

        manutencao_hardware_mw_large = util.atualizacao_linear(OPEX.MANUTENCAO_MW_LARGE.valor,
                                                               OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                               self.municipio.tempo_analise)

        manutencao_hardware_sw = util.atualizacao_linear(OPEX.MANUTENCAO_SW.valor,
                                                         OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                         self.municipio.tempo_analise)

        falhas += ((OPEX.MTTR_MW_LARGE.valor + (2.0 * self.municipio.tempo_viagem)) *
                    OPEX.QTD_TECNICOS.valor *
                    OPEX.QTD_TIMES.valor *
                    valor_salario_tecnico_ajustado +
                    manutencao_hardware_mw_large) * \
                    OPEX.TAXA_ARF_MW_LARGE.valor

        for ano, qtd_antena in enumerate(qtd_antena_mw):
            falha_small = np.zeros(self.municipio.tempo_analise)
            falha_sw = np.zeros(self.municipio.tempo_analise)
            if qtd_antena > 0 or qtd_sw_carrier_mw[ano] > 0:
                for t in range(ano, self.municipio.tempo_analise):
                    falha_small[t] += ((OPEX.MTTR_MW_SMALL.valor + (2.0 * self.municipio.tempo_viagem)) *
                                       OPEX.QTD_TECNICOS.valor *
                                       OPEX.QTD_TIMES.valor *
                                       valor_salario_tecnico_ajustado[t] +
                                       manutencao_hardware_mw_small[t]) * \
                                       OPEX.TAXA_ARF_MW_SMALL.valor
                    falha_small[t] += ((OPEX.MTTR_MW_SW.valor + (2.0 * self.municipio.tempo_viagem)) *
                                       OPEX.QTD_TECNICOS.valor *
                                       OPEX.QTD_TIMES.valor *
                                       valor_salario_tecnico_ajustado[t] +
                                       manutencao_hardware_sw[t]) * \
                                      OPEX.TAXA_ARF_MW_SMALL.valor
                falhas += falha_small

        return falhas

    def __calcula_capex_transporte(self):
        for ag in self.municipio.aglomerados:
            print('CAPEX de Transporte do Aglomerado {}:'.format(ag.id))
            for tipo in self.tipos_rede_radio:
                if tipo == 'Macro':
                    qtd_antena_mw = ag.qtd_antena_mw_pt_pt_macro_only
                    qtd_sw_carrier_mw = ag.qtd_sw_carrier_mw_macro_only
                    aglomerado = ag.capex_transporte_mw_macro
                    tco_transporte = self.capex_transporte_mw_macro
                else:
                    qtd_antena_mw = ag.qtd_antena_mw_pt_pt_hetnet
                    qtd_sw_carrier_mw = ag.qtd_sw_carrier_mw_hetnet
                    aglomerado = ag.capex_transporte_mw_hetnet
                    tco_transporte = self.capex_transporte_mw_hetnet

                equipamentos, instalacao = self.__calcula_capex_transporte_mw_implantacoes(qtd_antena_mw,
                                                                                           qtd_sw_carrier_mw)
                infraestrutura = self.__calcula_capex_transporte_mw_infraestrutura(qtd_antena_mw, tipo)

                aglomerado['equipamentos'] += equipamentos
                aglomerado['instalacao'] += instalacao
                aglomerado['infraestrutura'] += infraestrutura

                if ag.tipo_cenario == 'Original':
                    tco_transporte['infraestrutura'] += infraestrutura
                    tco_transporte['equipamentos'] += equipamentos
                    tco_transporte['instalacao'] += instalacao

                print('Implantação Transporte MW+{}'.format(tipo))
                print('CAPEX Transporte Infraestrutura:')
                print(infraestrutura)
                print('CAPEX Trasnporte Equipamentos:')
                print(equipamentos)
                print('CAPEX Transporte Instalação de Equipamentos:')
                print(instalacao)
                print()

    def __calcula_capex_transporte_mw_implantacoes(self, qtd_antena_mw, qtd_sw_carrier_mw):
        capex_transporte_instalacao = np.zeros(self.municipio.tempo_analise)
        capex_transporte_equipamentos = np.zeros(self.municipio.tempo_analise)

        # Realizar o cálculo de atualização do valor de salário do técnico de instalação ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                 CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        # Depois calcula-se a variacao do preço de aquisição de equipamentos ao longo dos anos
        hardware_mw_small = util.atualizacao_linear(CAPEX.ANTENA_MW_SMALL.valor,
                                                    CAPEX.TAXA_REAJUSTE.valor,
                                                    self.municipio.tempo_analise)

        hardware_sw = util.atualizacao_linear(CAPEX.SW_CARRIER.valor,
                                              CAPEX.TAXA_REAJUSTE.valor,
                                              self.municipio.tempo_analise)

        capex_transporte_equipamentos[0] += CAPEX.ANTENA_MW_LARGE.valor * 2.0

        # Deslocamento: Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
        despesas_deslocamento = self.municipio.tempo_viagem * \
                                CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                CAPEX.QTD_TIMES.valor * \
                                valor_salario_tecnico_ajustado * \
                                2.0

        # Mão-de-Obra: Multiplicar o tempo de atualização pelo salário do técnico e pela qtd de técnicos
        despesas_instalacao = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                              CAPEX.QTD_TIMES.valor * \
                              valor_salario_tecnico_ajustado[0] * \
                              (CAPEX.TEMPO_INSTALACAO_MW_LARGE.valor) * \
                              2.0

        capex_transporte_instalacao[0] += despesas_deslocamento[0] + despesas_instalacao

        for ano, qtd_antena in enumerate(qtd_antena_mw):
            if qtd_antena > 0 or qtd_sw_carrier_mw[ano] > 0:

                tempo_instalacao = CAPEX.TEMPO_INSTALACAO_MW_SMALL.valor * qtd_antena
                tempo_instalacao += CAPEX.TEMPO_INSTALACAO_SW.valor * qtd_sw_carrier_mw[ano]

                # Mão-de-Obra: Multiplicar o tempo de instalação pelo salário do técnico e pela qtd de técnicos
                despesas_instalacao = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                      CAPEX.QTD_TIMES.valor * \
                                      valor_salario_tecnico_ajustado[ano] * \
                                      tempo_instalacao

                capex_transporte_equipamentos[ano] += qtd_antena * hardware_mw_small[ano]
                capex_transporte_equipamentos[ano] += qtd_sw_carrier_mw[ano] * hardware_sw[ano]
                capex_transporte_instalacao[ano] += despesas_instalacao

                if ano != 0:
                    capex_transporte_instalacao[ano] += despesas_deslocamento[ano]

        return capex_transporte_equipamentos, capex_transporte_instalacao

    def __calcula_capex_transporte_mw_infraestrutura(self, qtd_antena_mw, tipo_rede_radio):
        capex_transporte_infraestrutura = np.zeros(self.municipio.tempo_analise)

        if tipo_rede_radio == 'Hetnet':
            for ano, qtd_antena in enumerate(qtd_antena_mw):
                if qtd_antena > 0:
                    qtd_hastes = (qtd_antena / 2.0)

                    # Realiza o cálculo de atualizacao do preco de aquisição por ano
                    infraestrutura_por_ano = util.atualizacao_linear(CAPEX.HASTE_MW.valor,
                                                                     CAPEX.TAXA_REAJUSTE.valor,
                                                                     self.municipio.tempo_analise)
                    infraestrutura_por_ano *= qtd_hastes

                    capex_transporte_infraestrutura[ano] += infraestrutura_por_ano[ano]

        return capex_transporte_infraestrutura
