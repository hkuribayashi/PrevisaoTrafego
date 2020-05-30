import numpy as np

from library.tco.Equipamento import Equipamento


class CAPEX:

    def __init__(self, municipio):
        self.municipio = municipio
        self.capex_backhaul = dict()
        self.capex_radio = dict()

    def calcula_capex(self):
        self.capex_radio['implantacao_macro'] = np.zeros(self.municipio.tempo_analise)
        self.capex_radio['implantacao_hetnet'] = np.zeros(self.municipio.tempo_analise)

        for ag in self.municipio.aglomerados:
            self.capex_radio['implantacao_macro'] += self.__calcula_capex_radio(ag.lista_bs['implantacao_macro'])
            self.capex_radio['implantacao_hetnet'] += self.__calcula_capex_radio(ag.lista_bs['implantacao_hetnet'])

    def __calcula_capex_radio(self, lista_bs):
        capex_radio = np.zeros(self.municipio.tempo_analise)

        # Contabilizar primeiramente as atualizações de BS
        # Se houver mais de uma atualização no mesmo ano, considerar apenas a última
        for b in lista_bs:
            if len(b.atualizacoes) > 0:
                b.ajuste_atualizacoesBS()
                print('Total de Atualizações: {}'.format(len(b.atualizacoes)))
                for at in b.atualizacoes:
                    # Aqui neste ponto se recupera o valor financeiro de cada atualizacao e coloca-se no respectivo
                    # Seria interessante realizar uma verificação do valor retornado por segurança e lançar uma
                    # exceção caso algo anormal acontecesse
                    # retorno = Equipamento.get_preco_atualizacao(at.tipo)
                    # if retorno < 0:
                    #   raise RuntimeError('[ERROR]: The parameter should be a positive value')
                    # else:
                    #   capex_radio[at.ano] += retorno
                    capex_radio[at.ano] += Equipamento.get_preco_atualizacao(at.tipo)
        return capex_radio
