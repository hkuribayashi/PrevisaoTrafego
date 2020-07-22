from library.custos.npv import NPV
from library.custos.tco_radio import TcoRadio
from library.custos.tco_transporte import TcoTransporte
from library.util.graficos import tco_simples, composicao_tco, composicao_tco_porcentagem, evolucao_tco, npv_municipio, \
    tco_municipio, fluxo_caixa_municipio
from library.util.util import get_cenarios_alternativos


class Engine:

    def __init__(self, municipios):
        self.municipios = municipios

        self.tco_radio = dict()
        self.tco_transporte = dict()
        self.npv = dict()

        for key in municipios:
            # Calcula Dimensionamento de Trafego e Rede para cada cenário
            print('Municipio/Cenário {}'.format(key))
            municipios[key].calcula_demanda_trafego()
            municipios[key].calcula_dimensionamento_rede_acesso()
            municipios[key].calcula_dimensionamento_rede_transporte()

            # Calcula TCO e NPV para cada cenário
            self.tco_radio[key] = TcoRadio(municipios[key])
            self.tco_transporte[key] = TcoTransporte(municipios[key])
            self.npv[key] = NPV(municipios[key])

    def run(self):
        for key in self.municipios:
            # Calcula o TCO de Rádio e Transporte
            self.tco_radio[key].get_tco()
            self.tco_transporte[key].get_tco()

        for key in self.municipios:
            # Calculo o Fluxo de Caixa
            self.npv[key].get_cf()

        for key in self.municipios:
            # Calculo o Valor Presente Líquido (VPL/NPV) e Payback
            self.npv[key].get_npv()

    def get_graficos(self):
        # self.__get_graficos_municipio()
        self.__get_graficos_aglomerados()

    def __get_graficos_municipio(self):
        # Gera gráficos de TCO
        tco_municipio(self.npv)

        # Gera gráficos de Fluxo de Caixa
        fluxo_caixa_municipio(self.npv)

        # Gera gráficos de NPV
        npv_municipio(self.npv)

    def __get_graficos_aglomerados(self):

        # Recupera os cenários e suas versões alternativas
        cenarios = get_cenarios_alternativos(self.municipios)

        # Gera Gráficos de Radio para Todos os Aglomerados
        for c in cenarios:
            tco_simples(c, 'Radio')
            composicao_tco(c, 'Radio')
            composicao_tco_porcentagem(c, 'Radio')
            evolucao_tco(c, 'Radio')

        # Gera Gráficos de Transporte para Todos os Aglomerados
        for c in cenarios:
            tco_simples(c, 'Transporte')
            composicao_tco(c, 'Transporte')
            composicao_tco_porcentagem(c, 'Transporte')
            evolucao_tco(c, 'Transporte')
