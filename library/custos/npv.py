import numpy as np

from library.custos.cf import CF


class NPV:

    def __init__(self, municipio):
        self.municipio = municipio
        self.assinaturas_moveis = np.zeros(self.municipio.tempo_analise)

        self.tco = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))
        self.cf = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))
        self.npv = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))

        self.payback = dict(macro=0.0, hetnet=0.0)

    def get_cf(self):
        for ag in self.municipio.aglomerados:
            if ag.tipo_cenario == 'Original':

                # Calcula o quantitativo de Termianais de Dados
                self.assinaturas_moveis += ag.total_terminais

                for tipo in self.municipio.tipos_rede_radio:
                    capex = np.zeros(self.municipio.tempo_analise)
                    opex = np.zeros(self.municipio.tempo_analise)

                    # Calcula o valor arrecadado com as assinaturas ao longo de 12 meses por ano
                    self.cf[tipo] += self.assinaturas_moveis * CF.TAXA_SUBSCRICAO.valor * 12.0

                    if tipo == 'Macro':
                        componente_capex = ag.capex_macro
                        componente_opex = ag.opex_macro
                    else:
                        componente_capex = ag.capex_hetnet
                        componente_opex = ag.opex_hetnet

                    # Recupera CAPEX e OPEX do Aglomerado Macro
                    capex += componente_capex['Radio']['infraestrutura']
                    capex += componente_capex['Radio']['equipamentos']
                    capex += componente_capex['Radio']['instalacao']

                    capex += componente_capex['Transporte']['infraestrutura']
                    capex += componente_capex['Transporte']['equipamentos']
                    capex += componente_capex['Transporte']['instalacao']

                    opex += componente_opex['Radio']['energia']
                    opex += componente_opex['Radio']['manutencao']
                    opex += componente_opex['Radio']['aluguel']
                    opex += componente_opex['Radio']['falhas']

                    opex += componente_opex['Transporte']['energia']
                    opex += componente_opex['Transporte']['manutencao']
                    opex += componente_opex['Transporte']['aluguel']
                    opex += componente_opex['Transporte']['falhas']

                    self.cf[tipo] = self.cf[tipo] - (capex + opex)
                    self.tco[tipo] += (capex + opex)

    def get_npv(self):
        for tipo in self.municipio.tipos_rede_radio:
            npv = np.zeros(self.municipio.tempo_analise)
            for ano, cf_ano in enumerate(self.cf[tipo]):
                tma = (1 + CF.TAXA_DESCONTO.valor) ** ano
                npv[ano] += (cf_ano / tma)

            for ano, npv_ano in enumerate(npv):
                if npv_ano > 0:
                    self.payback[tipo] = ano
                    break
            self.npv[tipo] = npv.sum()
