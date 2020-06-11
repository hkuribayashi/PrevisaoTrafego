import numpy as np

from library.tco.CAPEX import CAPEX
from library.tco.opex import OPEX
from library.util import util


class TCO:

    def __init__(self, municipio):
        self.municipio = municipio

        self.capex = CAPEX(municipio)

        # Despesas de OPEX de Radio
        self.opex_radio_macro = dict(energia=np.zeros(self.municipio.tempo_analise),
                                     manutencao=np.zeros(self.municipio.tempo_analise),
                                     aluguel=np.zeros(self.municipio.tempo_analise),
                                     falhas=np.zeros(self.municipio.tempo_analise))
        self.opex_radio_hetnet = dict(energia=np.zeros(self.municipio.tempo_analise),
                                      manutencao=np.zeros(self.municipio.tempo_analise),
                                      aluguel=np.zeros(self.municipio.tempo_analise),
                                      falhas=np.zeros(self.municipio.tempo_analise))

    def calcula_capex(self):
        self.capex.calcula_capex()

    def calcula_opex(self):
        for ag in self.municipio.aglomerados:
            print('OPEX de Rádio do Aglomerado {}:'.format(ag.id))
            energia = self.__calcula_opex_radio_energia(ag.lista_bs['implantacao_macro'])
            aluguel = self.__calcula_opex_radio_aluguel(ag.lista_bs['implantacao_macro'])
            manutencao = self.__calcula_opex_radio_manutencao(ag.lista_bs['implantacao_macro'])
            falhas = self.__calcula_opex_radio_falhas(ag.lista_bs['implantacao_macro'])

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
            opex_radio_energia_bs = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))
            for linha in range(b.ano, self.municipio.tempo_analise):
                # Faz o cálculo do volume de kWh por ano
                opex_radio_energia_bs[linha][linha] += (b.tipo_BS.potencia_transmissao / 1000.0) * \
                                                        tarifa_energia_ajustada[linha] * \
                                                        365.0 * \
                                                        24.0
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    # Realiza uma correção financeira no valor para analisá-lo no ano presente
                    opex_radio_energia_bs[linha][coluna] += opex_radio_energia_bs[linha][coluna - 1] * \
                                                            OPEX.TAXA_CORRECAO.valor
            # Achata a matriz somando todas as linhas e consolidando o valor associado a bs 'b' em opex_radio_energia
            opex_radio_energia += opex_radio_energia_bs.sum(axis=0)

        return opex_radio_energia

    def __calcula_opex_radio_aluguel(self, lista_bs):
        opex_radio_aluguel = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula a variacao do preco de alguel por m2 ao longo dos anos
        # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
        # Realiza-se o cálculo para Macro (Macro ou Micro) e para Small (Pico ou Femto), um vez que os valores estão
        # Definidos em valores de aluguel outdoor (Macro ou Micro) e indoor (Pico ou Femto)
        aluguel_area_macro_ajustado = util.atualizacao_linear(OPEX.ALUGUEL_OUTDOOR.valor,
                                                              OPEX.TAXA_REAJUSTE.valor,
                                                              self.municipio.tempo_analise)
        aluguel_area_small_ajustado = util.atualizacao_linear(OPEX.ALUGUEL_INDOOR.valor,
                                                              OPEX.TAXA_REAJUSTE.valor,
                                                              self.municipio.tempo_analise)

        for b in lista_bs:
            opex_radio_aluguel_m2 = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))
            for linha in range(b.ano, self.municipio.tempo_analise):
                if b.tipo_BS.tipo is 'Macro':
                    valor = aluguel_area_macro_ajustado[linha]
                elif b.tipo_BS.tipo is 'Micro':
                    valor = aluguel_area_macro_ajustado[linha]
                else:
                    valor = aluguel_area_small_ajustado[linha]
                opex_radio_aluguel_m2[linha][linha] += b.tipo_BS.area_fisica * valor
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    # Realiza uma correção financeira no valor para analisá-lo no ano presente
                    opex_radio_aluguel_m2[linha][coluna] += opex_radio_aluguel_m2[linha][coluna - 1] * \
                                                            OPEX.TAXA_CORRECAO.valor
            # Achata a matriz somando todas as linhas e consolidando o valor associado à bs 'b' em opex_radio_aluguel
            opex_radio_aluguel += opex_radio_aluguel_m2.sum(axis=0)

        return opex_radio_aluguel

    def __calcula_opex_radio_manutencao(self, lista_bs):
        opex_radio_manutencao = np.zeros(self.municipio.tempo_analise)
        opex_radio_viagens = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))

        # Assumimos que uma manutenção anual em cada BS
        for b in lista_bs:
            opex_radio_manutencao_bs = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))

            # Determinamos o valor base de manutenção de acordo com o tipo de BS
            if b.tipo_BS.tipo is 'Macro':
                valor_manutencao = OPEX.MANUTENCAO_MACRO.valor
            elif b.tipo_BS.tipo is 'Micro':
                valor_manutencao = OPEX.MANUTENCAO_MICRO.valor
            elif b.tipo_BS.tipo is 'Pico':
                valor_manutencao = OPEX.MANUTENCAO_PICO.valor
            else:
                valor_manutencao = OPEX.MANUTENCAO_FEMTO.valor

            # Realizar a atualizacao do valor de manutenção ajustado por ano
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_manutencao_ajustado = util.atualizacao_linear(valor_manutencao,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            for linha in range(b.ano, self.municipio.tempo_analise):
                opex_radio_manutencao_bs[linha][linha] += valor_manutencao_ajustado[linha]
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    # Realiza uma correção financeira no valor para analisá-lo no ano presente
                    opex_radio_manutencao_bs[linha][coluna] += opex_radio_manutencao_bs[linha][coluna - 1] * \
                                                               OPEX.TAXA_CORRECAO.valor

            # Achata a matriz somando todas as linhas e consolidando o valor associado a bs 'b' em opex_radio_energia
            opex_radio_manutencao += opex_radio_manutencao_bs.sum(axis=0)

        # Depois contabilizamos as viagens (uma viagem por ano)
        # Assumimos també que haverá uma 2 viagens (ida e volta) para cada time de técnicos e que este time
        # será capaz de realizar todas as manutenções de BSs do aglomerado

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        for linha in range(self.municipio.tempo_analise):
            opex_radio_viagens[linha][linha] += OPEX.DESLOCAMENTO.valor * \
                                                OPEX.QTD_TECNICOS.valor * \
                                                OPEX.SALARIO_TECNICO.valor * \
                                                valor_salario_tecnico_ajustado[linha] * \
                                                2.0
            for coluna in range(linha + 1, self.municipio.tempo_analise):
                # Realiza uma correção financeira no valor para analisá-lo no ano presente
                opex_radio_viagens[linha][coluna] += opex_radio_viagens[linha][coluna - 1] * \
                                                     OPEX.TAXA_CORRECAO.valor
        opex_radio_manutencao += opex_radio_viagens.sum(axis=0)

        return opex_radio_manutencao

    def __calcula_opex_radio_falhas(self, lista_bs):
        opex_radio_falhas = np.zeros(self.municipio.tempo_analise)
        return opex_radio_falhas
