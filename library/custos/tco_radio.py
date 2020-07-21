import numpy as np

from library.custos.capex import CAPEX
from library.custos.opex import OPEX
from library.custos.tco import TCO
from library.util import util


class TcoRadio(TCO):

    def __init__(self, municipio):
        componente = 'Radio'
        TCO.__init__(self, municipio, componente)

    def get_capex_atualizacoes(self, lista_bs):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        # Realizar o cálculo de atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                 CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar as atualizações de hardware das BS
            if len(b.atualizacoes) > 0:

                # Se houver mais de uma atualização no mesmo ano, considerar apenas a última
                b.ajuste_atualizacoesBS()

                for at in b.atualizacoes:

                    # Verifica qual o tipo de BS para contabilizar os custos de atualizacao
                    if b.tipo_BS.tipo == 'Macro':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_MACRO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_MACRO.valor
                    elif b.tipo_BS.tipo == 'Micro':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_MICRO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_MICRO.valor
                    elif b.tipo_BS.tipo == 'Femto':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_FEMTO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_FEMTO
                    else:
                        raise RuntimeError('Comportamento Inesperado: CAPEX - Tipo de BS não encontrada')

                    # Depois calcula-se a variacao do preço de atualização de hardware ao longo dos anos
                    atualizacao_hardware_ajustada = util.atualizacao_linear(atualizacao_hardware,
                                                                            CAPEX.TAXA_REAJUSTE.valor,
                                                                            self.municipio.tempo_analise)

                    # Pagasmento de Salários:
                    # Despesas de Instalação relativa ao tempo total de deslocamento e atualização
                    despesas_rh = CAPEX.QTD_TECNICOS_ATUALIZACAO.valor * \
                                  CAPEX.QTD_TIMES.valor * \
                                  valor_salario_tecnico_ajustado[at.ano] * \
                                  (tempo_atualizacao + (self.municipio.tempo_viagem * 2.0))

                    # Consolidar os valores no ano de atualização daquela BS
                    capex_radio_equipamentos[at.ano] += atualizacao_hardware_ajustada[at.ano]
                    capex_radio_instalacao[at.ano] += despesas_rh

        return capex_radio_equipamentos, capex_radio_instalacao

    def get_capex_implantacoes(self, lista_bs, lista_none=None):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        # Realizar o cálculo de atualização do valor de salário do técnico de instalação ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                 CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        for b in lista_bs:

            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            # Contabilizar o valor de cada BS com os custos de instsalação embutidos
            if b.existencia_previa is False:

                # Verifica qual o tipo de BS para contabilizar os custos de implantação
                if b.tipo_BS.tipo == 'Macro':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_MACRO.valor
                    if b.tipo_BS.tecnologia == '3G':
                        equipamento = CAPEX.MACRO_3G.valor
                    elif b.tipo_BS.tecnologia == '4G':
                        equipamento = CAPEX.MACRO_4G.valor
                    elif b.tipo_BS.tecnologia == '4.5G':
                        equipamento = CAPEX.MACRO_45G.valor
                    elif b.tipo_BS.tecnologia == '5G':
                        equipamento = CAPEX.MACRO_5G.valor
                    else:
                        raise RuntimeError('Comportamento Inesperado: CAPEX - Tecnologia Macro BS não encontrada')
                elif b.tipo_BS.tipo == 'Micro':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_MICRO.valor
                    if b.tipo_BS.tecnologia == '4G':
                        equipamento = CAPEX.MICRO_4G.valor
                    elif b.tipo_BS.tecnologia == '4.5G':
                        equipamento = CAPEX.MICRO_45G.valor
                    elif b.tipo_BS.tecnologia == '5G':
                        equipamento = CAPEX.MICRO_5G.valor
                    else:
                        raise RuntimeError('Comportamento Inesperado: CAPEX - Tecnologia Micro BS não encontrada')
                elif b.tipo_BS.tipo == 'Femto':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_FEMTO.valor
                    if b.tipo_BS.tecnologia == '4G':
                        equipamento = CAPEX.FEMTO_4G.valor
                    elif b.tipo_BS.tecnologia == '4.5G':
                        equipamento = CAPEX.FEMTO_45G.valor
                    elif b.tipo_BS.tecnologia == '5G':
                        equipamento = CAPEX.FEMTO_5G.valor
                    else:
                        raise RuntimeError('Comportamento Inesperado: CAPEX - Tecnologia Femto BS não encontrada')
                else:
                    raise RuntimeError('Comportamento Inesperado: CAPEX - Tipo de BS não encontrada')

                # Depois calcula-se a variacao do preço de atualização ao longo dos anos
                # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
                instalacao_hardware_ajustada = util.atualizacao_linear(equipamento,
                                                                       CAPEX.TAXA_REAJUSTE.valor,
                                                                       self.municipio.tempo_analise)

                # Pagasmento de Salários:
                # Despesas de Instalação relativa ao tempo total de deslocamento e atualização
                despesas_rh = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                              CAPEX.QTD_TIMES.valor * \
                              valor_salario_tecnico_ajustado[b.ano] * \
                              (tempo_instalacao + (self.municipio.tempo_viagem * 2.0))

                capex_radio_equipamentos[b.ano] += instalacao_hardware_ajustada[b.ano]
                capex_radio_instalacao[b.ano] += despesas_rh

        return capex_radio_equipamentos, capex_radio_instalacao

    def get_capex_infraestrutura(self, lista_bs, lista_none=None):
        capex_radio_infraesturtura = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            if b.existencia_previa is False:
                # Contabiliza os custos de infraestrutura:
                if b.tipo_BS.tipo is 'Macro':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_MACRO.valor
                elif b.tipo_BS.tipo is 'Micro':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_MICRO.valor
                elif b.tipo_BS.tipo == 'Femto':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_FEMTO.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: CAPEX - Tipo de BS não encontrada')

                # Realiza o cálculo de atualizacao do preco de aquisição por ano
                infraestrutura_por_ano = util.atualizacao_linear(custo_infraestrutura,
                                                                 CAPEX.TAXA_REAJUSTE.valor,
                                                                 self.municipio.tempo_analise)

                # Consolida o valor de infraestrutura no ano 'b.ano'
                capex_radio_infraesturtura[b.ano] += infraestrutura_por_ano[b.ano]

        return capex_radio_infraesturtura

    def get_opex_energia(self, lista_bs, lista_none=None):
        opex_radio_energia = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula-se a variacao da tarifa de energia ao longo dos anos
        tarifa_energia_ajustada = util.atualizacao_linear(OPEX.CONSUMO.valor,
                                                          OPEX.TAXA_REAJUSTE.valor,
                                                          self.municipio.tempo_analise)

        # Vamos assumir que todas as BS estão ligadas 24h/dia em 365 dias por ano, e depois computar o OPEX
        # Para cada BS se calcula o consumo a partir de seu ano de implantacao (bs.ano)
        for b in lista_bs:
            for ano in range(b.ano, self.municipio.tempo_analise):

                # Faz o cálculo do volume de $ por ano
                energia_ano = (b.tipo_BS.potencia_transmissao / 1000.0) * \
                              tarifa_energia_ajustada[ano] * \
                              365.0 * \
                              24.0

                opex_radio_energia[ano] += energia_ano

        return opex_radio_energia

    def get_opex_aluguel(self, lista_bs):
        opex_radio_aluguel = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula a variacao do preco de alguel por m2 ao longo dos anos
        aluguel_area_outdoor_ajustado = util.atualizacao_linear(OPEX.ALUGUEL_OUTDOOR.valor,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

        aluguel_area_indoor_ajustado = util.atualizacao_linear(OPEX.ALUGUEL_INDOOR.valor,
                                                               OPEX.TAXA_REAJUSTE.valor,
                                                               self.municipio.tempo_analise)

        for b in lista_bs:
            for ano in range(b.ano, self.municipio.tempo_analise):
                if b.tipo_BS.tipo is 'Macro':
                    valor = aluguel_area_outdoor_ajustado[ano]
                elif b.tipo_BS.tipo is 'Micro':
                    valor = aluguel_area_outdoor_ajustado[ano]
                elif b.tipo_BS.tipo is 'Femto':
                    valor = aluguel_area_indoor_ajustado[ano]
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tipo de BS não encontrada')

                aluguel_ano = b.tipo_BS.area_fisica * valor
                opex_radio_aluguel[ano] += aluguel_ano

        return opex_radio_aluguel

    def get_opex_manutencao(self, lista_bs, lista_none=None):
        opex_radio_manutencao = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        # Assumimos que uma manutenção anual em cada BS
        for b in lista_bs:
            # Determinamos o valor base de manutenção de acordo com o tipo de BS
            if b.tipo_BS.tipo == 'Macro':
                mttr = OPEX.MTTR_MACRO.valor
                if b.tipo_BS.tecnologia == '2G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_2G.valor
                elif b.tipo_BS.tecnologia == '3G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_3G.valor
                elif b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tecnologia Macro BS não encontrada')
            elif b.tipo_BS.tipo == 'Micro':
                mttr = OPEX.MTTR_MICRO.valor
                if b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tecnologia Micro BS não encontrada')
            elif b.tipo_BS.tipo == 'Femto':
                mttr = OPEX.MTTR_FEMTO.valor
                if b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tecnologia Femto BS não encontrada')
            else:
                raise RuntimeError('Comportamento Inesperado: OPEX - Tipo de BS não encontrada')

            # Realizar a atualizacao do valor de manutenção ajustado por ano
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_manutencao_ajustado = util.atualizacao_linear(valor_manutencao,
                                                                CAPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            for ano in range(b.ano, self.municipio.tempo_analise):
                despesa_rh = OPEX.QTD_TECNICOS.valor * \
                             OPEX.QTD_TIMES.valor * \
                             valor_salario_tecnico_ajustado[ano] * \
                             mttr
                opex_radio_manutencao[ano] += valor_manutencao_ajustado[ano] + despesa_rh

        # Depois contabilizamos as viagens (uma viagem por ano)
        for ano in range(self.municipio.tempo_analise):
            opex_radio_manutencao[ano] += self.municipio.tempo_viagem * \
                                          OPEX.QTD_TECNICOS.valor * \
                                          OPEX.QTD_TIMES.valor * \
                                          valor_salario_tecnico_ajustado[ano] * \
                                          2.0

        return opex_radio_manutencao

    def get_opex_falhas(self, lista_bs, lista_none=None):
        opex_radio_falhas = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        # Realizar a atualização do valor de taxa de penalidade por ano
        taxa_penalidade_ajustada = util.atualizacao_linear(OPEX.TAXA_PENALIDADE.valor,
                                                           OPEX.TAXA_REAJUSTE.valor,
                                                           self.municipio.tempo_analise)

        for b in lista_bs:

            # Determinamos os valores de AFR e MTTR de acordo com o tipo de BS
            if b.tipo_BS.tipo == 'Macro':
                afr = OPEX.TAXA_ARF_MACRO.valor
                mttr = OPEX.MTTR_MACRO.valor
                if b.tipo_BS.tecnologia == '2G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_2G.valor
                elif b.tipo_BS.tecnologia == '3G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_3G.valor
                elif b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_MACRO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tecnologia de Macro BS não encontrada')
            elif b.tipo_BS.tipo == 'Micro':
                afr = OPEX.TAXA_ARF_MICRO.valor
                mttr = OPEX.MTTR_MICRO.valor
                if b.tipo_BS.tecnologia == '3G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_3G.valor
                elif b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: CAPEX - Tecnologia de Micro BS não encontrada')
            elif b.tipo_BS.tipo == 'Femto':
                afr = OPEX.TAXA_ARF_FEMTO.valor
                mttr = OPEX.MTTR_FEMTO.valor
                if b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_FEMTO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: CAPEX - Tecnologia de Femto BS não encontrada')
            else:
                raise RuntimeError('Comportamento Inesperado: CAPEX - Tipo de BS não encontrada')

            # Realizar a atualizacao do valor de manutenção corretiva ajustado por ano
            valor_manutencao_ajustado = util.atualizacao_linear(valor_manutencao,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            for ano in range(b.ano, self.municipio.tempo_analise):
                opex_radio_falhas[ano] += ((mttr + 2.0 * self.municipio.tempo_viagem) *
                                           OPEX.QTD_TECNICOS.valor *
                                           OPEX.QTD_TIMES.valor *
                                           valor_salario_tecnico_ajustado[ano] + valor_manutencao_ajustado[ano]) * \
                                           afr

            # Cálculo de Falhas por BS de alta importânica
            # Assumimos 1 BS como sendo de alta importância por aglomerado
            # Esta BS é a BS marcada como Hub (True)
            if (b.hub_bs is True) and (self.municipio.tempo_medio_disponibilidade < OPEX.THRESHOLD_MACRO.valor):

                for ano in range(b.ano, self.municipio.tempo_analise):
                    opex_radio_falhas[ano] += (OPEX.THRESHOLD_MACRO.valor -
                                               self.municipio.tempo_medio_disponibilidade) * \
                                               taxa_penalidade_ajustada[ano]

        return opex_radio_falhas
