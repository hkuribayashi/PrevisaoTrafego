from library.custos.npv import NPV
from library.custos.tco_radio import TcoRadio
from library.custos.tco_transporte import TcoTransporte
from library.util.graficos import tco_simples, composicao_tco, composicao_tco_porcentagem, evolucao_tco, npv_municipio, \
    tco_municipio, fluxo_caixa_municipio
from library.util.util import get_cenarios_alternativos


class Engine:

    def __init__(self, municipio):
        self.municipio = municipio
        self.tco_radio = TcoRadio(municipio)
        self.tco_transporte = TcoTransporte(municipio)
        self.npv = NPV(municipio)

    def run(self):
        # Calcula o TCO de Rádio e Transporte
        self.tco_radio.get_tco()
        self.tco_transporte.get_tco()

        # Calculo o Fluxo de Caixa
        self.npv.get_cf()

        # Calculo o Valor Presente Líquido (VPL/NPV) e Payback
        self.npv.get_npv()

    def get_graficos(self):
        self.__get_graficos_municipio()
        self.__get_graficos_aglomerados()

    def __get_graficos_municipio(self):
        # Gera gráficos de TCO
        tco_municipio(self.npv.tco)

        # Gera gráficos de Fluxo de Caixa
        fluxo_caixa_municipio(self.npv.cf)

        # Gera gráficos de NPV
        npv_municipio(self.npv.npv)

    def __get_graficos_aglomerados(self):
        for ag in self.municipio.aglomerados:
            if ag.tipo_cenario == 'Original':
                # Recupera os cenários e suas versões alternativas
                cenarios = get_cenarios_alternativos(ag, self.municipio.aglomerados)

                # Gera Gráficos de Radio para Todos os Aglomerados
                tco_simples(cenarios, 'Radio')
                composicao_tco(cenarios, 'Radio')
                composicao_tco_porcentagem(cenarios, 'Radio')
                evolucao_tco(cenarios, 'Radio', self.tco_radio.tipos_rede_radio)

                # Gera Gráficos de Transporte para Todos os Aglomerados
                tco_simples(cenarios, 'Transporte')
                composicao_tco(cenarios, 'Transporte')
                composicao_tco_porcentagem(cenarios, 'Transporte')
                evolucao_tco(cenarios, 'Transporte', self.tco_transporte.tipos_rede_radio)
