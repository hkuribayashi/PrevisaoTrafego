import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from library.custos.capex import CAPEX
from library.custos.opex import OPEX
from library.util import util


class TCO:

    def __init__(self, municipio):
        self.municipio = municipio

        # Despesas de CAPEX de Radio
        self.capex_radio_macro = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                      equipamentos=np.zeros(self.municipio.tempo_analise),
                                      instalacao=np.zeros(self.municipio.tempo_analise))
        self.capex_radio_hetnet = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                       equipamentos=np.zeros(self.municipio.tempo_analise),
                                       instalacao=np.zeros(self.municipio.tempo_analise))

        # Despesas de OPEX de Radio Macro
        self.opex_radio_macro = dict(energia=np.zeros(self.municipio.tempo_analise),
                                     manutencao=np.zeros(self.municipio.tempo_analise),
                                     aluguel=np.zeros(self.municipio.tempo_analise),
                                     falhas=np.zeros(self.municipio.tempo_analise))

        # Despesas de OPEX de Radio Hetnet
        self.opex_radio_hetnet = dict(energia=np.zeros(self.municipio.tempo_analise),
                                      manutencao=np.zeros(self.municipio.tempo_analise),
                                      aluguel=np.zeros(self.municipio.tempo_analise),
                                      falhas=np.zeros(self.municipio.tempo_analise))

    def calcula_capex(self):
        self.__calcula_capex_radio()

    def calcula_opex(self):
        self.__calcula_opex_radio()

    def __calcula_capex_radio(self):
        for ag in self.municipio.aglomerados:
            print('CAPEX de Rádio do Aglomerado {}:'.format(ag.id))

            equipamentos_atualizacao, instalacao_atualizacao = self.__calcula_capex_radio_atualizacoes(
                ag.lista_bs['implantacao_macro'])
            equipamentos_novos, instalacao_novos = self.__calcula_capex_radio_implantacaoes(
                ag.lista_bs['implantacao_macro'])
            infraestrutura = self.__calcula_capex_radio_infraestrutura(ag.lista_bs['implantacao_macro'])

            ag.capex_radio_macro['infraestrutura'] += infraestrutura
            ag.capex_radio_macro['equipamentos'] += equipamentos_atualizacao
            ag.capex_radio_macro['equipamentos'] += equipamentos_novos
            ag.capex_radio_macro['instalacao'] += instalacao_atualizacao
            ag.capex_radio_macro['instalacao'] += instalacao_novos

            if ag.tipo_cenario == 'Original':
                self.capex_radio_macro['infraestrutura'] += infraestrutura
                self.capex_radio_macro['equipamentos'] += equipamentos_atualizacao
                self.capex_radio_macro['equipamentos'] += equipamentos_novos
                self.capex_radio_macro['instalacao'] += instalacao_atualizacao
                self.capex_radio_macro['instalacao'] += instalacao_novos

            print('Implantação Macro Only')
            print('CAPEX Radio Infraestrutura:')
            print(infraestrutura)
            print('CAPEX Radio Equipamentos Novos:')
            print(equipamentos_novos)
            print('CAPEX Radio Equipamentos Atualizados:')
            print(equipamentos_atualizacao)
            print('CAPEX Radio Instalação de Equipamentos Novos:')
            print(instalacao_novos)
            print('CAPEX Radio Instalação de Atualização de Equipamentos:')
            print(instalacao_atualizacao)
            print()

            equipamentos_atualizacao, instalacao_atualizacao = self.__calcula_capex_radio_atualizacoes(
                ag.lista_bs['implantacao_hetnet'])
            equipamentos_novos, instalacao_novos = self.__calcula_capex_radio_implantacaoes(
                ag.lista_bs['implantacao_hetnet'])
            infraestrutura = self.__calcula_capex_radio_infraestrutura(ag.lista_bs['implantacao_hetnet'])

            ag.capex_radio_hetnet['infraestrutura'] += infraestrutura
            ag.capex_radio_hetnet['equipamentos'] += equipamentos_atualizacao
            ag.capex_radio_hetnet['equipamentos'] += equipamentos_novos
            ag.capex_radio_hetnet['instalacao'] += instalacao_atualizacao
            ag.capex_radio_hetnet['instalacao'] += instalacao_novos

            if ag.tipo_cenario == 'Original':
                self.capex_radio_hetnet['infraestrutura'] += infraestrutura
                self.capex_radio_hetnet['equipamentos'] += equipamentos_atualizacao
                self.capex_radio_hetnet['equipamentos'] += equipamentos_novos
                self.capex_radio_hetnet['instalacao'] += instalacao_atualizacao
                self.capex_radio_hetnet['instalacao'] += instalacao_novos

            print('Implantação Hetnet')
            print('CAPEX Infraestrutura:')
            print(infraestrutura)
            print('CAPEX Equipamentos Novos:')
            print(equipamentos_novos)
            print('CAPEX Equipamentos Atualizados:')
            print(equipamentos_atualizacao)
            print('CAPEX Instalação de Equipamentos Novos:')
            print(instalacao_novos)
            print('CAPEX Instalação de Atualização de Equipamentos:')
            print(instalacao_atualizacao)
            print()

    def __calcula_capex_radio_atualizacoes(self, lista_bs):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar as atualizações de hardware das BS
            # Se houver mais de uma atualização no mesmo ano, considerar apenas a última
            if len(b.atualizacoes) > 0:
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

                    # Depois calcula-se a variacao do preço de atualização ao longo dos anos
                    # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
                    atualizacao_hardware_ajustada = util.atualizacao_linear(atualizacao_hardware,
                                                                            CAPEX.TAXA_REAJUSTE.valor,
                                                                            self.municipio.tempo_analise)

                    # Realizar o cálculo de atualização do valor de salário do técnico de manutenção ajustado por ano
                    valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                             CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                             self.municipio.tempo_analise)

                    # Despesas de Instalação: Deslocamento + Mão-de-Obra
                    # Deslocamento:
                    # Assumimos també que haverá uma 2 viagens (ida e volta) para cada time de técnicos necessários
                    # Calcula os custos de deslocamento para a atualização das BSs
                    # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                    despesas_deslocamento = self.municipio.tempo_viagem * \
                                            CAPEX.QTD_TECNICOS_ATUALIZACAO.valor * \
                                            CAPEX.QTD_TIMES.valor * \
                                            valor_salario_tecnico_ajustado[at.ano] * \
                                            2.0

                    # Mão-de-Obra:
                    # Multiplicar o tempo de atualização pelo salário do técnico e pela qtd de técnicos
                    despesas_instalacao = CAPEX.QTD_TECNICOS_ATUALIZACAO.valor * \
                                          CAPEX.QTD_TIMES.valor * \
                                          valor_salario_tecnico_ajustado[at.ano] * \
                                          tempo_atualizacao

                    # Consolidar os valores no ano de atualização daquela BS
                    capex_radio_equipamentos[at.ano] += atualizacao_hardware_ajustada[at.ano]
                    capex_radio_instalacao[at.ano] += despesas_instalacao + despesas_deslocamento

        return capex_radio_equipamentos, capex_radio_instalacao

    def __calcula_capex_radio_implantacaoes(self, lista_bs):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            # Contabilizar o valor de cada BS com os custos de instsalação embutidos
            if b.existencia_previa is False:
                # Calcula os custos de deslocamento para a implantação das BSs
                # Realizar o cálculo de atualização do valor de salário do técnico de instalação ajustado por ano
                valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                         CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                         self.municipio.tempo_analise)

                # Instalação: Deslocamento + Mão-de-Obra
                # Deslocamento:
                # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                despesas_deslocamento = self.municipio.tempo_viagem * \
                                        CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                        CAPEX.QTD_TIMES.valor * \
                                        valor_salario_tecnico_ajustado[b.ano] * \
                                        2.0

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

                # Mão-de-Obra:
                # Multiplicar o tempo de atualização pelo salário do técnico e pela qtd de técnicos
                despesas_instalacao = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                      CAPEX.QTD_TIMES.valor * \
                                      valor_salario_tecnico_ajustado[b.ano] * \
                                      tempo_instalacao

                # Depois calcula-se a variacao do preço de atualização ao longo dos anos
                # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
                instalacao_hardware_ajustada = util.atualizacao_linear(equipamento,
                                                                       CAPEX.TAXA_REAJUSTE.valor,
                                                                       self.municipio.tempo_analise)

                capex_radio_equipamentos[b.ano] += instalacao_hardware_ajustada[b.ano]
                capex_radio_instalacao[b.ano] += despesas_instalacao + despesas_deslocamento

        return capex_radio_equipamentos, capex_radio_instalacao

    def __calcula_capex_radio_infraestrutura(self, lista_bs):
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

    def __calcula_opex_radio(self):
        for ag in self.municipio.aglomerados:
            print('OPEX de Rádio do Aglomerado {}:'.format(ag.id))
            energia = self.__calcula_opex_radio_energia(ag.lista_bs['implantacao_macro'])
            aluguel = self.__calcula_opex_radio_aluguel(ag.lista_bs['implantacao_macro'])
            manutencao = self.__calcula_opex_radio_manutencao(ag.lista_bs['implantacao_macro'])
            falhas = self.__calcula_opex_radio_falhas(ag.lista_bs['implantacao_macro'])

            ag.opex_radio_macro['energia'] += energia
            ag.opex_radio_macro['manutencao'] += manutencao
            ag.opex_radio_macro['aluguel'] += aluguel
            ag.opex_radio_macro['falhas'] += falhas

            if ag.tipo_cenario == 'Original':
                self.opex_radio_macro['energia'] += energia
                self.opex_radio_macro['manutencao'] += manutencao
                self.opex_radio_macro['aluguel'] += aluguel
                self.opex_radio_macro['falhas'] += falhas

            print('Implantação Macro Only')
            print('OPEX Energia:')
            print(energia)
            print('OPEX manutencao:')
            print(manutencao)
            print('OPEX aluguel:')
            print(aluguel)
            print('OPEX falhas:')
            print(falhas)
            print()

            energia = self.__calcula_opex_radio_energia(ag.lista_bs['implantacao_hetnet'])
            aluguel = self.__calcula_opex_radio_aluguel(ag.lista_bs['implantacao_hetnet'])
            manutencao = self.__calcula_opex_radio_manutencao(ag.lista_bs['implantacao_hetnet'])
            falhas = self.__calcula_opex_radio_falhas(ag.lista_bs['implantacao_hetnet'])

            ag.opex_radio_hetnet['energia'] += energia
            ag.opex_radio_hetnet['manutencao'] += manutencao
            ag.opex_radio_hetnet['aluguel'] += aluguel
            ag.opex_radio_hetnet['falhas'] += falhas

            if ag.tipo_cenario == 'Original':
                self.opex_radio_hetnet['energia'] += energia
                self.opex_radio_hetnet['manutencao'] += manutencao
                self.opex_radio_hetnet['aluguel'] += aluguel
                self.opex_radio_hetnet['falhas'] += falhas

            print('Implantação Hetnet')
            print('OPEX Energia:')
            print(energia)
            print('OPEX manutencao:')
            print(manutencao)
            print('OPEX aluguel:')
            print(aluguel)
            print('OPEX falhas:')
            print(falhas)
            print()

    def __calcula_opex_radio_energia(self, lista_bs):
        opex_radio_energia = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula-se a variacao da tarifa de energia ao longo dos anos
        # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
        tarifa_energia_ajustada = util.atualizacao_linear(OPEX.CONSUMO.valor,
                                                          OPEX.TAXA_REAJUSTE.valor,
                                                          self.municipio.tempo_analise)

        # Vamos assumir que todas as BS estão ligadas 24h/dia em 365 dias por ano, e depois computar o OPEX
        # ao longo dos anos por BS. Para cada BS se calcula o consumo a partir de seu ano de implantacao (bs.ano)
        for b in lista_bs:
            for ano in range(b.ano, self.municipio.tempo_analise):
                # Faz o cálculo do volume de kWh por ano
                opex_radio_energia[ano] += (b.tipo_BS.potencia_transmissao / 1000.0) * \
                                           tarifa_energia_ajustada[ano] * \
                                           365.0 * \
                                           24.0

        return opex_radio_energia

    def __calcula_opex_radio_aluguel(self, lista_bs):
        opex_radio_aluguel = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula a variacao do preco de alguel por m2 ao longo dos anos
        # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
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

    def __calcula_opex_radio_manutencao(self, lista_bs):
        opex_radio_manutencao = np.zeros(self.municipio.tempo_analise)

        # Assumimos que uma manutenção anual em cada BS
        for b in lista_bs:
            # Determinamos o valor base de manutenção de acordo com o tipo de BS
            if b.tipo_BS.tipo == 'Macro':
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
                if b.tipo_BS.tecnologia == '4G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_4G.valor
                elif b.tipo_BS.tecnologia == '4.5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_45G.valor
                elif b.tipo_BS.tecnologia == '5G':
                    valor_manutencao = OPEX.MANUTENCAO_MICRO_5G.valor
                else:
                    raise RuntimeError('Comportamento Inesperado: OPEX - Tecnologia Micro BS não encontrada')
            elif b.tipo_BS.tipo == 'Femto':
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
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            for ano in range(b.ano, self.municipio.tempo_analise):
                opex_radio_manutencao[ano] += valor_manutencao_ajustado[ano]

        # Depois contabilizamos as viagens (uma viagem por ano)
        # Assumimos també que haverá uma 2 viagens (ida e volta) para cada time de técnicos e que este time
        # será capaz de realizar todas as manutenções de BSs do aglomerado

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        for ano in range(self.municipio.tempo_analise):
            opex_radio_manutencao[ano] += self.municipio.tempo_viagem * \
                                          OPEX.QTD_TECNICOS.valor * \
                                          OPEX.QTD_TIMES.valor * \
                                          valor_salario_tecnico_ajustado[ano] * \
                                          2.0

        return opex_radio_manutencao

    def __calcula_opex_radio_falhas(self, lista_bs):
        opex_radio_falhas = np.zeros(self.municipio.tempo_analise)

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
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_manutencao_ajustado = util.atualizacao_linear(valor_manutencao,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                     OPEX.TAXA_CORRECAO_SALARARIO.valor,
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

                # Realizar a atualização do valor de taxa de penalidade por ano
                # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
                taxa_penalidade_ajustada = util.atualizacao_linear(OPEX.TAXA_PENALIDADE.valor,
                                                                   OPEX.TAXA_REAJUSTE.valor,
                                                                   self.municipio.tempo_analise)

                for ano in range(b.ano, self.municipio.tempo_analise):
                    opex_radio_falhas[ano] += (OPEX.THRESHOLD_MACRO.valor -
                                               self.municipio.tempo_medio_disponibilidade) * \
                                              taxa_penalidade_ajustada[ano]

        return opex_radio_falhas

    def gera_graficos(self):
        # Gerar gráficos para cada aglomerado
        #for ag in self.municipio.aglomerados:
        #    print('Gráficos do Aglomerado {}:'.format(ag.id))
        #    self.__gera_graficos_evolucao_tco(ag, 'Aglomerado', ag.id)
        #    self.__gera_graficos_tco_acumulado(ag, 'Aglomerado', ag.id)
        #    self.__gera_graficos_composicao_tco_porcentagem(ag, 'Aglomerado', ag.id)
        #    plt.show()

        # Gerar gráficos consolidados para o Município
        # self.__gera_graficos_evolucao_tco(self, 'Município', 'Faro - PA')
        # self.__gera_graficos_tco_acumulado(self, 'Município', 'Faro - PA')
        # self.__gera_graficos_composicao_tco_porcentagem(self, 'Municipio', 'Faro - PA')
        # plt.show()

        # Gera gráficos de comparação entre Greenfield e Brownfield
        for ag in self.municipio.aglomerados:
            cenarios = dict()
            if ag.tipo_cenario == 'Original':
                cenarios['Original'] = ag
                for outros_ag in self.municipio.aglomerados:
                    if outros_ag.tipo_cenario == 'Alternativo' and outros_ag.cenario_original.id == ag.id:
                        cenarios['Alternativo'+str(outros_ag.id)] = outros_ag
                self.__gera_grafico_comparacao_(cenarios)
                self.__gera_graficos_composicao_tco(cenarios)
                plt.show()

    def __gera_graficos_composicao_tco(self, cenarios):
        global nome_aglomerado

        infraestrutura = list()
        equipamentos = list()
        instalacao = list()
        energia = list()
        manutencao = list()
        aluguel = list()
        falhas = list()

        rotulos = list()

        for key in cenarios:
            infraestrutura.append(cenarios[key].capex_radio_macro['infraestrutura'].sum())
            infraestrutura.append(cenarios[key].capex_radio_hetnet['infraestrutura'].sum())

            equipamentos.append(cenarios[key].capex_radio_macro['equipamentos'].sum())
            equipamentos.append(cenarios[key].capex_radio_hetnet['equipamentos'].sum())

            instalacao.append(cenarios[key].capex_radio_macro['instalacao'].sum())
            instalacao.append(cenarios[key].capex_radio_hetnet['instalacao'].sum())

            energia.append(cenarios[key].opex_radio_macro['energia'].sum())
            energia.append(cenarios[key].opex_radio_hetnet['energia'].sum())

            manutencao.append(cenarios[key].opex_radio_macro['manutencao'].sum())
            manutencao.append(cenarios[key].opex_radio_hetnet['manutencao'].sum())

            aluguel.append(cenarios[key].opex_radio_macro['aluguel'].sum())
            aluguel.append(cenarios[key].opex_radio_hetnet['aluguel'].sum())

            falhas.append(cenarios[key].opex_radio_macro['falhas'].sum())
            falhas.append(cenarios[key].opex_radio_hetnet['falhas'].sum())

            rotulos.append('Macro-C' + str(cenarios[key].id))
            rotulos.append('Hetnet-C' + str(cenarios[key].id))

            if cenarios[key].tipo_cenario == 'Original':
                nome_aglomerado = cenarios[key].tipo_aglomerado

        # Posição das Barras no eixo X
        posicao = list()
        if len(cenarios) <= 2:
            separacao = 2.5
            plt.figure(figsize=(8.0, 5.5))
            bar_width = 1.0
        else:
            separacao = 3.8
            plt.figure(figsize=(9.0, 5.5))
            bar_width = 2.0

        for i in range(2 * len(cenarios)):
            posicao.append(i * separacao)

        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Aluguel', 'Falhas']
        line_width = 0.5

        plt.bar(posicao, infraestrutura, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

        plt.bar(posicao, equipamentos, bottom=infraestrutura, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)

        plt.bar(posicao, instalacao, bottom=[i + j for i, j in zip(infraestrutura, equipamentos)], color='#88a54f',
                edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

        plt.bar(posicao, energia, bottom=[i + j + k for i, j, k in zip(infraestrutura, equipamentos, instalacao)],
                color='#72578f', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(posicao, manutencao,
                bottom=[i + j + k + l for i, j, k, l in zip(infraestrutura, equipamentos, instalacao, energia)],
                color='#4298ae',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(posicao, aluguel,
                bottom=[i + j + k + l + m for i, j, k, l, m in
                        zip(infraestrutura, equipamentos, instalacao, energia, manutencao)],
                color='#da8436',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(posicao, falhas,
                bottom=[i + j + k + l + m + n for i, j, k, l, m, n in
                        zip(infraestrutura, equipamentos, instalacao, energia, manutencao, aluguel)],
                color='#93a9cf',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)

        # Custom X an Y axis
        plt.xticks(posicao, rotulos)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=7)
        plt.title('Composição TCO Rádio Aglomerado {}'.format(nome_aglomerado))
        plt.ylabel('Composição do TCO (Unidades Monetárias $)')

    def __gera_grafico_comparacao_(self, cenarios):
        capex = list()
        opex = list()

        rotulos = list()
        global nome_aglomerado

        for key in cenarios:
            capex_macro = np.zeros(self.municipio.tempo_analise)
            capex_macro += cenarios[key].capex_radio_macro['infraestrutura']
            capex_macro += cenarios[key].capex_radio_macro['equipamentos']
            capex_macro += cenarios[key].capex_radio_macro['instalacao']

            capex_hetnet = np.zeros(self.municipio.tempo_analise)
            capex_hetnet += cenarios[key].capex_radio_hetnet['infraestrutura']
            capex_hetnet += cenarios[key].capex_radio_hetnet['equipamentos']
            capex_hetnet += cenarios[key].capex_radio_hetnet['instalacao']

            opex_macro = np.zeros(self.municipio.tempo_analise)
            opex_macro += cenarios[key].opex_radio_macro['energia']
            opex_macro += cenarios[key].opex_radio_macro['manutencao']
            opex_macro += cenarios[key].opex_radio_macro['aluguel']
            opex_macro += cenarios[key].opex_radio_macro['falhas']

            opex_hetnet = np.zeros(self.municipio.tempo_analise)
            opex_hetnet += cenarios[key].opex_radio_hetnet['energia']
            opex_hetnet += cenarios[key].opex_radio_hetnet['manutencao']
            opex_hetnet += cenarios[key].opex_radio_hetnet['aluguel']
            opex_hetnet += cenarios[key].opex_radio_hetnet['falhas']

            capex.append(capex_macro.sum())
            capex.append(capex_hetnet.sum())
            opex.append(opex_macro.sum())
            opex.append(opex_hetnet.sum())

            rotulos.append('Macro-C'+str(cenarios[key].id))
            rotulos.append('Hetnet-C'+str(cenarios[key].id))

            if cenarios[key].tipo_cenario == 'Original':
                nome_aglomerado = cenarios[key].tipo_aglomerado

        # Posição das Barras no eixo X
        posicao = list()
        if len(cenarios) <= 2:
            separacao = 2.5
            plt.figure()
            bar_width = 1.0
        else:
            separacao = 3.8
            plt.figure(figsize=(9.0, 5.5))
            bar_width = 2.0
        for i in range(2 * len(cenarios)):
            posicao.append(i * separacao)

        # Legendas e Largura das Barras
        legenda = ['CAPEX Radio', 'OPEX Radio']

        line_width = 0.5

        plt.bar(posicao, capex, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(posicao, opex, bottom=capex, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)

        # Alterações nas propriedades dos Eixos X e Y
        plt.xticks(posicao, rotulos)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('TCO (Unidades Monetárias $)')
        plt.title('Comparação TCO: Aglomerado {}'.format(nome_aglomerado))

    def __gera_graficos_evolucao_tco(self, entidade, tipo_entidade, id_entidade):
        plt.figure()

        capex_macro = np.zeros(self.municipio.tempo_analise)
        capex_macro += entidade.capex_radio_macro['infraestrutura']
        capex_macro += entidade.capex_radio_macro['equipamentos']
        capex_macro += entidade.capex_radio_macro['instalacao']

        capex_hetnet = np.zeros(self.municipio.tempo_analise)
        capex_hetnet += entidade.capex_radio_hetnet['infraestrutura']
        capex_hetnet += entidade.capex_radio_hetnet['equipamentos']
        capex_hetnet += entidade.capex_radio_hetnet['instalacao']

        opex_macro = np.zeros(self.municipio.tempo_analise)
        opex_macro += entidade.opex_radio_macro['energia']
        opex_macro += entidade.opex_radio_macro['manutencao']
        opex_macro += entidade.opex_radio_macro['aluguel']
        opex_macro += entidade.opex_radio_macro['falhas']

        opex_hetnet = np.zeros(self.municipio.tempo_analise)
        opex_hetnet += entidade.opex_radio_hetnet['energia']
        opex_hetnet += entidade.opex_radio_hetnet['manutencao']
        opex_hetnet += entidade.opex_radio_hetnet['aluguel']
        opex_hetnet += entidade.opex_radio_hetnet['falhas']

        # The position of the bars on the x-axis
        r = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0]

        # Legendas
        names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        legenda = ['CAPEX Radio', 'OPEX Radio']
        bar_width = 1.6
        line_width = 0.5

        plt.bar(r, capex_macro, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, opex_macro, bottom=capex_macro, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)

        # Custom X axis
        plt.xticks(r, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('TCO (Unidades Monetárias $)')
        plt.xlabel('Unidade de Tempo (t)')
        plt.title('Evolução do TCO ao longo dos ano - Macro: {} {}'.format(tipo_entidade, id_entidade))
        plt.figure()

        # Gerar gráfico de evolução do TCO ao longo dos anos - Hetnet
        plt.bar(r, capex_hetnet, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, opex_hetnet, bottom=capex_hetnet, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)

        # Custom X axis
        plt.xticks(r, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('TCO (Unidades Monetárias $)')
        plt.xlabel('Unidade de Tempo (t)')
        plt.title('Evolução do TCO ao longo dos ano - Hetnet: {} {}'.format(tipo_entidade, id_entidade))

    def __gera_graficos_tco_acumulado(self, entidade, tipo_entidade, id_entidade):
        plt.figure()

        # Gerar gráfico de TCO para os diversos cenários existentes
        capex_macro = np.zeros(self.municipio.tempo_analise)
        capex_macro += entidade.capex_radio_macro['infraestrutura']
        capex_macro += entidade.capex_radio_macro['equipamentos']
        capex_macro += entidade.capex_radio_macro['instalacao']

        capex_hetnet = np.zeros(self.municipio.tempo_analise)
        capex_hetnet += entidade.capex_radio_hetnet['infraestrutura']
        capex_hetnet += entidade.capex_radio_hetnet['equipamentos']
        capex_hetnet += entidade.capex_radio_hetnet['instalacao']

        opex_macro = np.zeros(self.municipio.tempo_analise)
        opex_macro += entidade.opex_radio_macro['energia']
        opex_macro += entidade.opex_radio_macro['manutencao']
        opex_macro += entidade.opex_radio_macro['aluguel']
        opex_macro += entidade.opex_radio_macro['falhas']

        opex_hetnet = np.zeros(self.municipio.tempo_analise)
        opex_hetnet += entidade.opex_radio_hetnet['energia']
        opex_hetnet += entidade.opex_radio_hetnet['manutencao']
        opex_hetnet += entidade.opex_radio_hetnet['aluguel']
        opex_hetnet += entidade.opex_radio_hetnet['falhas']

        # Values of each group
        capex = [capex_macro.sum(), 0, capex_hetnet.sum(), 0]
        opex = [opex_macro.sum(), 0, opex_hetnet.sum(), 0]

        # The position of the bars on the x-axis
        r = [0, 2.5, 5.0, 7.5]

        # Names of group and bar width
        names = ['Macro', '', 'Hetnet', '']
        legenda = ['CAPEX Radio', 'OPEX Radio']
        bar_width = 1.0
        line_width = 0.5

        plt.bar(r, capex, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, opex, bottom=capex, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)

        # Custom X an Y axis
        plt.xticks(r, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('TCO (Unidades Monetárias $)')
        plt.title('TCO da Rede Acesso - Macro e Hetnet: {} {}'.format(tipo_entidade, id_entidade))

    def __gera_graficos_composicao_tco_porcentagem(self, entidade, tipo_entidade, id_entidade):
        plt.figure(figsize=(8, 5.5))

        capex_macro = np.zeros(self.municipio.tempo_analise)
        capex_macro += entidade.capex_radio_macro['infraestrutura']
        capex_macro += entidade.capex_radio_macro['equipamentos']
        capex_macro += entidade.capex_radio_macro['instalacao']

        capex_hetnet = np.zeros(self.municipio.tempo_analise)
        capex_hetnet += entidade.capex_radio_hetnet['infraestrutura']
        capex_hetnet += entidade.capex_radio_hetnet['equipamentos']
        capex_hetnet += entidade.capex_radio_hetnet['instalacao']

        opex_macro = np.zeros(self.municipio.tempo_analise)
        opex_macro += entidade.opex_radio_macro['energia']
        opex_macro += entidade.opex_radio_macro['manutencao']
        opex_macro += entidade.opex_radio_macro['aluguel']
        opex_macro += entidade.opex_radio_macro['falhas']

        opex_hetnet = np.zeros(self.municipio.tempo_analise)
        opex_hetnet += entidade.opex_radio_hetnet['energia']
        opex_hetnet += entidade.opex_radio_hetnet['manutencao']
        opex_hetnet += entidade.opex_radio_hetnet['aluguel']
        opex_hetnet += entidade.opex_radio_hetnet['falhas']

        # Data
        raw_data = {'infraestrutura': [entidade.capex_radio_macro['infraestrutura'].sum(),
                                       entidade.capex_radio_hetnet['infraestrutura'].sum(),
                                       0.00001,
                                       0.00001],
                    'equipamentos': [entidade.capex_radio_macro['equipamentos'].sum(),
                                     entidade.capex_radio_hetnet['equipamentos'].sum(),
                                     0.00001,
                                     0.00001],
                    'instalacao': [entidade.capex_radio_macro['instalacao'].sum(),
                                   entidade.capex_radio_hetnet['instalacao'].sum(),
                                   0.00001,
                                   0.00001],
                    'energia': [entidade.opex_radio_macro['energia'].sum(),
                                entidade.opex_radio_hetnet['energia'].sum(),
                                0.00001,
                                0.00001],
                    'manutencao': [entidade.opex_radio_macro['manutencao'].sum(),
                                   entidade.opex_radio_hetnet['manutencao'].sum(),
                                   0.00001,
                                   0.00001],
                    'aluguel': [entidade.opex_radio_macro['aluguel'].sum(),
                                entidade.opex_radio_hetnet['aluguel'].sum(),
                                0.00001,
                                0.00001],
                    'falhas': [entidade.opex_radio_macro['falhas'].sum(),
                               entidade.opex_radio_hetnet['falhas'].sum(),
                               0.00001,
                               0.00001]}

        df = pd.DataFrame(raw_data)

        # The position of the bars on the x-axis
        r = [0, 2.5, 5.0, 7.5, 10.0, 12.5]
        bar_width = 1.0
        line_width = 0.5

        # From raw value to percentage
        totals = [i + j + k + l + m + n + o for i, j, k, l, m, n, o in
                  zip(df['infraestrutura'], df['equipamentos'], df['instalacao'], df['energia'], df['manutencao'],
                      df['aluguel'], df['falhas'])]
        infraestrutura = [i / j * 100 for i, j in zip(df['infraestrutura'], totals)]
        equipamentos = [i / j * 100 for i, j in zip(df['equipamentos'], totals)]
        instalacao = [i / j * 100 for i, j in zip(df['instalacao'], totals)]

        energia = [i / j * 100 for i, j in zip(df['energia'], totals)]
        manutencao = [i / j * 100 for i, j in zip(df['manutencao'], totals)]
        aluguel = [i / j * 100 for i, j in zip(df['aluguel'], totals)]
        falhas = [i / j * 100 for i, j in zip(df['falhas'], totals)]

        infraestrutura[2] = 0
        infraestrutura[3] = 0
        infraestrutura.append(0)
        infraestrutura.append(0)

        equipamentos[2] = 0
        equipamentos[3] = 0
        equipamentos.append(0)
        equipamentos.append(0)

        instalacao[2] = 0
        instalacao[3] = 0
        instalacao.append(0)
        instalacao.append(0)

        energia[2] = 0
        energia[3] = 0
        energia.append(0)
        energia.append(0)

        manutencao[2] = 0
        manutencao[3] = 0
        manutencao.append(0)
        manutencao.append(0)

        aluguel[2] = 0
        aluguel[3] = 0
        aluguel.append(0)
        aluguel.append(0)

        falhas[2] = 0
        falhas[3] = 0
        falhas.append(0)
        falhas.append(0)

        # Create green Bars
        plt.bar(r, infraestrutura, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        # Create orange Bars
        plt.bar(r, equipamentos, bottom=infraestrutura, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
                linewidth=line_width)
        # Create blue Bars
        plt.bar(r, instalacao, bottom=[i + j for i, j in zip(infraestrutura, equipamentos)], color='#88a54f',
                edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, energia, bottom=[i + j + k for i, j, k in zip(infraestrutura, equipamentos, instalacao)],
                color='#72578f', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, manutencao,
                bottom=[i + j + k + l for i, j, k, l in zip(infraestrutura, equipamentos, instalacao, energia)],
                color='#4298ae',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, aluguel,
                bottom=[i + j + k + l + m for i, j, k, l, m in
                        zip(infraestrutura, equipamentos, instalacao, energia, manutencao)],
                color='#da8436',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)
        plt.bar(r, falhas,
                bottom=[i + j + k + l + m + n for i, j, k, l, m, n in
                        zip(infraestrutura, equipamentos, instalacao, energia, manutencao, aluguel)],
                color='#93a9cf',
                edgecolor='black',
                width=bar_width, zorder=3, linewidth=line_width)

        names = ['Macro', 'Hetnet', 'Fibra', 'MW', 'SFV On-grid', 'SFV Híbrido']
        plt.xticks(r, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Aluguel', 'Falhas']
        plt.legend(legenda, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=7)
        plt.title('Composição TCO - Rádio, Transporte e SFV: {} {}'.format(tipo_entidade, id_entidade))
        plt.ylabel('Composição do TCO (%)')
