import numpy as np

from library.tco.Aluguel import Aluguel
from library.tco.Energia import Energia
from library.util import Util


class OPEX:

    def __init__(self, municipio):
        self.municipio = municipio
        self.opex_backhaul = dict()

        # Despesas de CAPEX de Radio
        self.opex_radio_macro = dict(energia=np.zeros(self.municipio.tempo_analise),
                                     manutencao=np.zeros(self.municipio.tempo_analise),
                                     aluguel=np.zeros(self.municipio.tempo_analise))
        self.opex_radio_hetnet = dict(energia=np.zeros(self.municipio.tempo_analise),
                                      manutencao=np.zeros(self.municipio.tempo_analise),
                                      aluguel=np.zeros(self.municipio.tempo_analise))

    def calcula_opex(self, capex):
        for ag in self.municipio.aglomerados:
            print('OPEX de Rádio do Aglomerado {}:'.format(ag.id))
            energia, manutencao, aluguel = self.__calcula_opex_radio(ag.lista_bs['implantacao_macro'], capex.capex_radio_macro)
            self.opex_radio_macro['energia'] += energia
            self.opex_radio_macro['manutencao'] += manutencao
            self.opex_radio_macro['aluguel'] += aluguel
            print('Implantação Macro Only')
            print('OPEX Energia:')
            print(energia)
            print('OPEX manutencao:')
            print(manutencao)
            print('OPEX aluguel:')
            print(aluguel)
            print()

            energia, manutencao, aluguel = self.__calcula_opex_radio(ag.lista_bs['implantacao_hetnet'], capex.capex_radio_hetnet)
            self.opex_radio_macro['energia'] += energia
            self.opex_radio_macro['manutencao'] += manutencao
            self.opex_radio_macro['aluguel'] += aluguel
            print('Implantação Hetnet')
            print('OPEX Energia:')
            print(energia)
            print('OPEX manutencao:')
            print(manutencao)
            print('OPEX aluguel:')
            print(aluguel)
            print()

    def __calcula_opex_radio(self, lista_bs, capex_radio):
        opex_radio_energia = np.zeros(self.municipio.tempo_analise)
        opex_radio_aluguel = np.zeros(self.municipio.tempo_analise)
        opex_radio_manutencao = np.zeros(self.municipio.tempo_analise)

        # Calcula a despesas de Consumo de Energia
        # Vamos assumir que todas as BS estão ligadas 24h/dia em 365 dias por ano
        # E depois computar o OPEX ao longo dos anos por BS

        # Primeiro se calcula a variacao da tarifa de energia ao longo dos ano
        # Considera-se um reajuste anual de 3% (0.03) em cima do valor do ano 0
        # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
        tarifa_energia_por_ano = Util.atualizacao_preco_linear(Energia.CONSUMO.valor, 0.03, self.municipio.tempo_analise)

        # Para cada BS se calcula o consumo a partir de seu ano de implantacao (bs.ano)
        for b in lista_bs:
            opex_radio_energia_bs = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))
            for linha in range(b.ano, self.municipio.tempo_analise):
                opex_radio_energia_bs[linha][linha] = (b.tipo_BS.potencia_transmissao/1000.0) * \
                                                      tarifa_energia_por_ano[linha] * \
                                                      365.0 * 24.0
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    opex_radio_energia_bs[linha][coluna] += opex_radio_energia_bs[linha][coluna-1] * 1.01
            opex_radio_energia += opex_radio_energia_bs.sum(axis=0)

        # Agora computar as despesas de aluguel de terreno para as BSs
        # Primeiro se calcula a variacao do preco de alguel por m2 ao longo dos anos
        # Considera-se um reajuste anual de 3% (0.03) em cima do valor do ano 0
        # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
        # Realiza-se o cálculo para Macro (Macro ou Micro) e para Small (Pico ou Femto), um vez que os valores estão
        # Definidos em valores de aluguel outdoor (Macro ou Micro) e indoor (Pico ou Femto)
        # Aqui este trecho de código deve ser refatorado para adotar o termo 00.3 (3%) a.a. como um parâmetro ajustável
        aluguel_area_macro = Util.atualizacao_preco_linear(Aluguel.OUTDOOR.valor, 0.03, self.municipio.tempo_analise)
        aluguel_area_small = Util.atualizacao_preco_linear(Aluguel.INDOOR.valor, 0.03, self.municipio.tempo_analise)

        for b in lista_bs:
            opex_radio_aluguel_m2 = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))
            for linha in range(b.ano, self.municipio.tempo_analise):
                if b.tipo_BS.tipo is 'Macro' or 'Micro':
                    valor = aluguel_area_macro[linha]
                else:
                    valor = aluguel_area_small[linha]
                opex_radio_aluguel_m2[linha][linha] = b.tipo_BS.area_fisica * valor
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    # Deve ser refatorado para adotar o termo 0.01 (1%) a.a. como um parâmetro ajustável
                    opex_radio_aluguel_m2[linha][coluna] += opex_radio_aluguel_m2[linha][coluna-1] * 1.01
                opex_radio_aluguel += opex_radio_aluguel_m2.sum(axis=0)

        # Agora computar as despesas com manutenção da rede rádio
        # Estamos assumindo que os valores de manutenção proativa são 10% dos valores de CAPEX
        # Aqui este trecho de código deve ser refatorado para adotar o termo 0.1 (10%) como um parâmetro ajustável
        opex_radio_manutencao = capex_radio['infraestrutura'] * 0.1 + capex_radio['equipamentos'] * 0.1

        return opex_radio_energia, opex_radio_aluguel, opex_radio_manutencao
