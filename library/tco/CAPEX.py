import numpy as np

from library.tco.Equipamento import Equipamento
from library.tco.InfraEquipamento import InfraRadio
from library.tco.InstalacaoGeral import InstalacaoRadio, InstalacaoGeral
from library.util import Util


class CAPEX:

    def __init__(self, municipio):
        self.municipio = municipio
        self.capex_backhaul = dict()

        #Despesas de CAPEX de Radio
        self.capex_radio_macro = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                      equipamentos=np.zeros(self.municipio.tempo_analise))
        self.capex_radio_hetnet = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                      equipamentos=np.zeros(self.municipio.tempo_analise))

    def calcula_capex(self):
        for ag in self.municipio.aglomerados:
            infra, equipamentos = self.__calcula_capex_radio(ag.lista_bs['implantacao_macro'])
            self.capex_radio_macro['infraestrutura'] += infra
            self.capex_radio_macro['equipamentos'] += equipamentos

            infra, equipamentos = self.__calcula_capex_radio(ag.lista_bs['implantacao_hetnet'])
            self.capex_radio_hetnet['infraestrutura'] += infra
            self.capex_radio_hetnet['equipamentos'] += equipamentos

    def __calcula_capex_radio(self, lista_bs):
        capex_radio_infraesturtura = np.zeros(self.municipio.tempo_analise)
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar primeiramente as atualizações de BS
            # Se houver mais de uma atualização no mesmo ano, considerar apenas a última
            if len(b.atualizacoes) > 0:
                b.ajuste_atualizacoesBS()
                for at in b.atualizacoes:
                    # Aqui neste ponto se recupera o valor financeiro de cada atualizacao e coloca-se no respectivo
                    # Seria interessante realizar uma verificação do valor retornado por segurança e lançar uma
                    # exceção caso algo anormal acontecesse
                    # retorno = Equipamento.get_preco_atualizacao(at.tipo)
                    # if retorno < 0:
                    #   raise RuntimeError('[ERROR]: The parameter should be a positive value')
                    # else:
                    #   capex_radio_equipamentos[at.ano] += retorno

                    # Verifica qual o tipo de BS para contabilizar os custos de atualizacao
                    if b.tipo_BS.tipo is 'Macro':
                        instalacao = InstalacaoRadio.ATUALIZACAO_MACRO.preco_unitario
                    else:
                        instalacao = InstalacaoRadio.ATUALIZACAO_SMALL.preco_unitario

                    # Calcula os custos de deslocamento para a atualização das BSs
                    # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                    despesas_deslocamento = 2.0 * InstalacaoGeral.DESLOCAMENTO.preco_unitario * \
                                                  InstalacaoGeral.DESLOCAMENTO.quantidade_tecnicos * \
                                                  InstalacaoGeral.TECNICO.preco_unitario

                    preco_atualizado = Util.variacao_preco_linear(Equipamento.get_preco_atualizacao(at.tipo) +
                                                                  instalacao +
                                                                  despesas_deslocamento,
                                                                  -0.03, self.municipio.tempo_analise - at.ano)
                    for ano, preco_ano in enumerate(preco_atualizado):
                        capex_radio_equipamentos[ano + at.ano] += preco_ano

            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            # Contabilizar o valor de cada BS com os custos de instsalação embutidos
            if b.existencia_previa is False:

                # Calcula os custos de deslocamento para a atualização das BSs
                # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                despesas_deslocamento = 2.0 * InstalacaoGeral.DESLOCAMENTO.preco_unitario * \
                                        InstalacaoGeral.DESLOCAMENTO.quantidade_tecnicos * \
                                        InstalacaoGeral.TECNICO.preco_unitario

                # Verifica qual o tipo de BS para contabilizar os custos de atualizacao
                if b.tipo_BS.tipo is 'Macro':
                    instalacao = InstalacaoRadio.MACRO.preco_unitario
                else:
                    instalacao = InstalacaoRadio.SMALL.preco_unitario

                # Contabiliza os custos dos equipamentos de Rádio (Macro ou Small Cell)
                equipamentos_depreciado_por_ano = Util.variacao_preco_linear(Equipamento.MBS.preco_unitario + instalacao +
                                                                      despesas_deslocamento,
                                                                      -0.03,
                                                                      self.municipio.tempo_analise - b.ano)

                # Contabiliza os custos de infraestrutura:
                # Por enquanto, estamos contabilizando apenas os custos de implantação da torre (cell site)
                if b.tipo_BS.tipo is 'Macro':
                    infraestrutura = InfraRadio.TORRE_MACRO.preco_unitario
                elif b.tipo_BS.tipo is 'Micro':
                    infraestrutura = InfraRadio.TORRE_MICRO.preco_unitario
                else:
                    infraestrutura = InfraRadio.TORRE_SMALL.preco_unitario

                # Realiza o cálculo de depreciação da infraestrutura implantada
                infraestrutura_depreciada_por_ano = Util.variacao_preco_linear(infraestrutura, -0.03,
                                                                               self.municipio.tempo_analise - b.ano)
                for ano, equipamento_ano in enumerate(equipamentos_depreciado_por_ano):
                    capex_radio_equipamentos[ano + b.ano] += equipamento_ano
                    capex_radio_infraesturtura[ano + b.ano] += infraestrutura_depreciada_por_ano[ano]

        return capex_radio_infraesturtura, capex_radio_equipamentos
