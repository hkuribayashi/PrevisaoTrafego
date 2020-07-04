import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from library.custos.radio import CapexRadio, OpexRadio


class TCO:

    def __init__(self, municipio):
        self.municipio = municipio
        self.capex_radio = CapexRadio(municipio)
        self.opex_radio = OpexRadio(municipio)

    def gera_graficos(self):
        # Gerar gráficos para cada aglomerado
        # Gráficos de TCO
        for ag in self.municipio.aglomerados:
            print('Gráficos do Aglomerado {}:'.format(ag.id))
            self.__gera_graficos_evolucao_tco(ag, 'Aglomerado', ag.id)
            self.__gera_graficos_tco_acumulado(ag, 'Aglomerado', ag.id)
            self.__gera_graficos_composicao_tco(ag, 'Aglomerado', ag.id)
            plt.show()

        # Gerar gráficos consolidados para o Município
        # Gráficos de TCO
        # self.__gera_graficos_tco(self, 'Município', 'Faro - PA')

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

    def __gera_graficos_composicao_tco(self, entidade, tipo_entidade, id_entidade):
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
