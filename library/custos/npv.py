import numpy as np

from library.custos.cf import CF


class NPV:

    def __init__(self, municipio):
        self.municipio = municipio
        self.assinaturas_moveis = np.zeros(self.municipio.tempo_analise)

        self.tco = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))
        self.cf = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))
        self.npv = dict(Macro=np.zeros(self.municipio.tempo_analise), Hetnet=np.zeros(self.municipio.tempo_analise))

        self.payback = dict(Macro=0.0, Hetnet=0.0)

    def get_cf(self):
        for ag in self.municipio.aglomerados:
            # Calcula o quantitativo de Termianais de Dados
            self.assinaturas_moveis += ag.total_terminais
            print()

        arreacadacao = self.assinaturas_moveis * CF.TAXA_SUBSCRICAO.valor * 12.0
        print('Valor de Arrecadação: ')
        print(arreacadacao)
        print(arreacadacao.sum())

        capex = np.zeros(self.municipio.tempo_analise)
        opex = np.zeros(self.municipio.tempo_analise)

        for ag in self.municipio.aglomerados:

            # Recupera CAPEX e OPEX do Aglomerado Macro
            capex += ag.capex_macro['Radio']['infraestrutura']
            capex += ag.capex_macro['Radio']['equipamentos']
            capex += ag.capex_macro['Radio']['instalacao']
            capex += ag.capex_macro['Transporte']['infraestrutura']
            capex += ag.capex_macro['Transporte']['equipamentos']
            capex += ag.capex_macro['Transporte']['instalacao']

            opex += ag.opex_macro['Radio']['energia']
            opex += ag.opex_macro['Radio']['manutencao']
            opex += ag.opex_macro['Radio']['aluguel']
            opex += ag.opex_macro['Radio']['falhas']
            opex += ag.opex_macro['Transporte']['energia']
            opex += ag.opex_macro['Transporte']['manutencao']
            opex += ag.opex_macro['Transporte']['aluguel']
            opex += ag.opex_macro['Transporte']['falhas']

        self.cf['Macro'] = arreacadacao - (capex + opex)
        self.tco['Macro'] += (capex + opex)

        capex = np.zeros(self.municipio.tempo_analise)
        opex = np.zeros(self.municipio.tempo_analise)

        for ag in self.municipio.aglomerados:

            # Recupera CAPEX e OPEX do Aglomerado Hetnet
            capex += ag.capex_hetnet['Radio']['infraestrutura']
            capex += ag.capex_hetnet['Radio']['equipamentos']
            capex += ag.capex_hetnet['Radio']['instalacao']
            capex += ag.capex_hetnet['Transporte']['infraestrutura']
            capex += ag.capex_hetnet['Transporte']['equipamentos']
            capex += ag.capex_hetnet['Transporte']['instalacao']

            opex += ag.opex_hetnet['Radio']['energia']
            opex += ag.opex_hetnet['Radio']['manutencao']
            opex += ag.opex_hetnet['Radio']['aluguel']
            opex += ag.opex_hetnet['Radio']['falhas']
            opex += ag.opex_hetnet['Transporte']['energia']
            opex += ag.opex_hetnet['Transporte']['aluguel']
            opex += ag.opex_hetnet['Transporte']['falhas']

        self.cf['Hetnet'] = arreacadacao - (capex + opex)
        self.tco['Hetnet'] += (capex + opex)

        print('TCO:')
        print('Macro:')
        print(self.tco['Macro'])
        print(self.tco['Macro'].sum())
        print('CF:')
        print('Macro:')
        print(self.cf['Macro'])

        print('TCO:')
        print('Hetnet:')
        print(self.tco['Hetnet'])
        print(self.tco['Hetnet'].sum())
        print('CF:')
        print('Hetnet:')
        print(self.cf['Hetnet'])



    def get_npv(self):
        print('NPV')
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

            print('Implantação {}:'.format(tipo))
            print(self.npv[tipo])
            print()
