from library.custos.tco_radio import TcoRadio
from library.custos.tco_transporte import TcoTransporte
from library.util.graficos import tco_simples, composicao_tco, composicao_tco_porcentagem, evolucao_tco
from library.util.util import get_cenarios_alternativos


class TCO:

    def __init__(self, municipio):
        self.municipio = municipio
        self.path = '/Users/hugo/Desktop/'
        self.tipos_rede_radio = ['Macro', 'Hetnet']

        self.tco_radio = TcoRadio(municipio)
        self.tco_transporte = TcoTransporte(municipio)

        self.tco_radio.get_tco()
        self.tco_transporte.get_tco()

    def gera_graficos(self):

        for ag in self.municipio.aglomerados:
            if ag.tipo_cenario == 'Original':
                # Recupera os cenários e suas versões alternativas
                cenarios = get_cenarios_alternativos(ag, self.municipio.aglomerados)

                # Gera Gráficos de Radio para Todos os Aglomerados
                tco_simples(cenarios, 'Radio', self.path)
                composicao_tco(cenarios, 'Radio', self.path)
                composicao_tco_porcentagem(cenarios, 'Radio', self.path)
                evolucao_tco(cenarios, 'Radio', self.tipos_rede_radio, self.path)

                # Gera Gráficos de Transporte para Todos os Aglomerados
                tco_simples(cenarios, 'Transporte', self.path)
                composicao_tco(cenarios, 'Transporte', self.path)
                composicao_tco_porcentagem(cenarios, 'Transporte', self.path)
                evolucao_tco(cenarios, 'Transporte', self.tipos_rede_radio, self.path)
