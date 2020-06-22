import numpy as np

from library.custos.capex import CAPEX
from library.custos.opex import OPEX
from library.util import util


class TCO:

    def __init__(self, municipio):
        self.municipio = municipio

        # Despesas de CAPEX de Radio
        self.capex_radio_macro = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                      equipamentos=np.zeros(self.municipio.tempo_analise),
                                      instalacao=np.zeros(self.municipio.tempo_analise))
        self.capex_radio_hetnet = dict(infraestrutura=np.zeros(self.municipio.tempo_analise),
                                       equipamentos=np.zeros(self.municipio.tempo_analise),
                                       instalacao=np.zeros(self.municipio.tempo_analise))

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
        for ag in self.municipio.aglomerados:
            print('CAPEX de Rádio do Aglomerado {}:'.format(ag.id))

            equipamentos_atualizacao, instalacao_atualizacao = self.__calcula_capex_radio_atualizacoes(ag.lista_bs['implantacao_macro'])
            equipamentos_novos, instalacao_novos = self.__calcula_capex_radio_implantacaoes(ag.lista_bs['implantacao_macro'])
            infraestrutura = self.__calcula_capex_radio_infraestrutura(ag.lista_bs['implantacao_macro'])
            self.capex_radio_macro['infraestrutura'] += infraestrutura
            self.capex_radio_macro['equipamentos'] += equipamentos_atualizacao
            self.capex_radio_macro['equipamentos'] += equipamentos_novos
            self.capex_radio_macro['instalacao'] += instalacao_atualizacao
            self.capex_radio_macro['instalacao'] += instalacao_novos

            print('Implantação Macro Only')
            print('CAPEX Infraestrutura:')
            print(infraestrutura)
            print('CAPEX Equipamentos Novos:')
            print(equipamentos_novos)
            print('CAPEX Equipamentos Atualizados:')
            print(equipamentos_atualizacao)
            print('CAPEX Instalação de Equipamentos Novos:')
            print(instalacao_novos)
            print('CAPEX Instalação de Atualização de Equipamentos:')
            print(instalacao_atualizacao)
            print()

            equipamentos_atualizacao, instalacao_atualizacao = self.__calcula_capex_radio_atualizacoes(ag.lista_bs['implantacao_hetnet'])
            equipamentos_novos, instalacao_novos = self.__calcula_capex_radio_implantacaoes(ag.lista_bs['implantacao_hetnet'])
            infraestrutura = self.__calcula_capex_radio_infraestrutura(ag.lista_bs['implantacao_hetnet'])
            self.capex_radio_hetnet['infraestrutura'] += infraestrutura
            self.capex_radio_hetnet['equipamentos'] += equipamentos_atualizacao
            self.capex_radio_hetnet['equipamentos'] += equipamentos_novos
            self.capex_radio_hetnet['instalacao'] += instalacao_atualizacao
            self.capex_radio_hetnet['instalacao'] += instalacao_novos

            print('Implantação Hetnet')
            print('CAPEX Infraestrutura:')
            print(infraestrutura)
            print('CAPEX Equipamentos Novos:')
            print(equipamentos_novos)
            print('CAPEX Equipamentos Atualizados:')
            print(equipamentos_atualizacao)
            print('CAPEX Instalação de Equipamentos Novos:')
            print(instalacao_novos)
            print('CAPEX Instalação de Atualização de Equipamentos:')
            print(instalacao_atualizacao)
            print()

    def __calcula_capex_radio_atualizacoes(self, lista_bs):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar as atualizações de hardware das BS
            # Se houver mais de uma atualização no mesmo ano, considerar apenas a última
            if len(b.atualizacoes) > 0:
                b.ajuste_atualizacoesBS()

                capex_radio_equipamentos_bs = np.zeros(self.municipio.tempo_analise)
                capex_radio_instalacao_bs = np.zeros(self.municipio.tempo_analise)

                for at in b.atualizacoes:
                    # Verifica qual o tipo de BS para contabilizar os custos de atualizacao
                    if b.tipo_BS.tipo is 'Macro':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_MACRO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_MACRO.valor
                    elif b.tipo_BS.tipo is 'Micro':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_MICRO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_MICRO.valor
                    elif b.tipo_BS.tipo is 'Pico':
                        atualizacao_hardware = CAPEX.ATUALIZACAO_PICO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_MICRO
                    else:
                        atualizacao_hardware = CAPEX.ATUALIZACAO_FEMTO.valor
                        tempo_atualizacao = CAPEX.TEMPO_ATUALIZACAO_FEMTO

                    # Depois calcula-se a variacao do preço de atualização ao longo dos anos
                    # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
                    atualizacao_hardware_ajustada = util.atualizacao_linear(atualizacao_hardware,
                                                                            CAPEX.TAXA_REAJUSTE.valor,
                                                                            self.municipio.tempo_analise)

                    # Realizar o cálculo de atualização do valor de salário do técnico de manutenção ajustado por ano
                    valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                             CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                             self.municipio.tempo_analise)

                    # Despesas de Instalação: Deslocamento + Mão-de-Obra
                    # Deslocamento:
                    # Assumimos també que haverá uma 2 viagens (ida e volta) para cada time de técnicos necessários
                    # Calcula os custos de deslocamento para a atualização das BSs
                    # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                    despesas_deslocamento = self.municipio.tempo_viagem * \
                                            CAPEX.QTD_TECNICOS_ATUALIZACAO.valor * \
                                            CAPEX.QTD_TIMES.valor * \
                                            valor_salario_tecnico_ajustado[b.ano] * \
                                            2.0

                    # Mão-de-Obra:
                    # Multiplicar o tempo de atualização pelo salário do técnico e pela qtd de técnicos
                    despesas_instalacao = CAPEX.QTD_TECNICOS_ATUALIZACAO.valor * \
                                          CAPEX.QTD_TIMES.valor * \
                                          valor_salario_tecnico_ajustado[b.ano] * \
                                          tempo_atualizacao

                    # Consolidar os valores no ano de atualização daquela BS
                    capex_radio_equipamentos_bs[b.ano] += atualizacao_hardware_ajustada[b.ano]
                    capex_radio_instalacao_bs[b.ano] += despesas_instalacao + despesas_deslocamento

                    # Faz uma depreciação anual de 5% (verificar pametro na classe CAPEX)
                    # Para corrigir o valor do hardware ao longo do tempo
                    for ano in range(b.ano + 1, self.municipio.tempo_analise):
                        capex_radio_equipamentos_bs[ano] += capex_radio_equipamentos_bs[ano - 1] * \
                                                         (1 + CAPEX.TAXA_DEPRECIACAO.valor)
                        capex_radio_instalacao_bs[ano] += capex_radio_instalacao_bs[ano - 1] * \
                                                          (1 + CAPEX.TAXA_DEPRECIACAO.valor)
                    capex_radio_equipamentos += capex_radio_equipamentos_bs
                    capex_radio_instalacao += capex_radio_instalacao_bs

        return capex_radio_equipamentos, capex_radio_instalacao

    def __calcula_capex_radio_implantacaoes(self, lista_bs):
        capex_radio_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_radio_instalacao = np.zeros(self.municipio.tempo_analise)

        for b in lista_bs:
            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            # Contabilizar o valor de cada BS com os custos de instsalação embutidos
            if b.existencia_previa is False:

                capex_radio_equipamentos_bs = np.zeros(self.municipio.tempo_analise)
                capex_radio_instalacao_bs = np.zeros(self.municipio.tempo_analise)

                # Calcula os custos de deslocamento para a implantação das BSs
                # Realizar o cálculo de atualização do valor de salário do técnico de instalação ajustado por ano
                valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                         CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                         self.municipio.tempo_analise)

                # Instalação: Deslocamento + Mão-de-Obra
                # Deslocamento:
                # Contabiliza duas viagens (ida e volta) para a quantidade de técnicos necessária
                despesas_deslocamento = self.municipio.tempo_viagem * \
                                        CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                        CAPEX.QTD_TIMES.valor * \
                                        valor_salario_tecnico_ajustado[b.ano] * \
                                        2.0

                # Verifica qual o tipo de BS para contabilizar os custos de implantação
                if b.tipo_BS.tipo is 'Macro':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_MACRO.valor
                    equipamento = CAPEX.MACRO.valor
                elif b.tipo_BS.tipo is 'Micro':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_MICRO.valor
                    equipamento = CAPEX.MICRO.valor
                elif b.tipo_BS.tipo is 'Pico':
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_PICO.valor
                    equipamento = CAPEX.PICO.valor
                else:
                    tempo_instalacao = CAPEX.TEMPO_INSTALACAO_FEMTO.valor
                    equipamento = CAPEX.FEMTO.valor

                # Mão-de-Obra:
                # Multiplicar o tempo de atualização pelo salário do técnico e pela qtd de técnicos
                despesas_instalacao = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                                      CAPEX.QTD_TIMES.valor * \
                                      valor_salario_tecnico_ajustado[b.ano] * \
                                      tempo_instalacao

                # Depois calcula-se a variacao do preço de atualização ao longo dos anos
                # Observar o parâmetro alpha da equacao (1.1) de Yaghoubi et al (2019).
                instalacao_hardware_ajustada = util.atualizacao_linear(equipamento,
                                                                       CAPEX.TAXA_REAJUSTE.valor,
                                                                       self.municipio.tempo_analise)

                capex_radio_equipamentos_bs[b.ano] += instalacao_hardware_ajustada[b.ano]
                capex_radio_instalacao_bs[b.ano] += despesas_instalacao + despesas_deslocamento

                # Faz uma depreciação anual de 5% (verificar pametro na classe CAPEX)
                # Para corrigir o valor do hardware ao longo do tempo
                for ano in range(b.ano + 1, self.municipio.tempo_analise):
                    capex_radio_equipamentos_bs[ano] += capex_radio_equipamentos_bs[ano - 1] * \
                                                        (1 + CAPEX.TAXA_DEPRECIACAO.valor)
                    capex_radio_instalacao_bs[ano] += capex_radio_instalacao_bs[ano - 1] * \
                                                      (1 + CAPEX.TAXA_DEPRECIACAO.valor)
                capex_radio_equipamentos += capex_radio_equipamentos_bs
                capex_radio_instalacao += capex_radio_instalacao_bs

        return capex_radio_equipamentos, capex_radio_instalacao

    def __calcula_capex_radio_infraestrutura(self, lista_bs):
        capex_radio_infraesturtura = np.zeros(self.municipio.tempo_analise)
        for b in lista_bs:

            capex_radio_infraesturtura_bs = np.zeros(self.municipio.tempo_analise)

            # Contabilizar quantas BS novas foram implantadas ao longo dos anos e seu valor no CAPEX
            if b.existencia_previa is False:
                # Contabiliza os custos de infraestrutura:
                if b.tipo_BS.tipo is 'Macro':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_MACRO.valor
                elif b.tipo_BS.tipo is 'Micro':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_MICRO.valor
                elif b.tipo_BS.tipo is 'Pico':
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_PICO.valo
                else:
                    custo_infraestrutura = CAPEX.INFRAESTRUTURA_FEMTO.valor

                # Realiza o cálculo de atualizacao do preco de aquisição por ano
                infraestrutura_por_ano = util.atualizacao_linear(custo_infraestrutura,
                                                                 CAPEX.TAXA_REAJUSTE.valor,
                                                                 self.municipio.tempo_analise)
                # Consolida o valor de infraestrutura no ano 'b.ano'
                capex_radio_infraesturtura_bs[b.ano] += infraestrutura_por_ano[b.ano]

                # Faz uma depreciação anual de 5% (verificar pametro na classe CAPEX)
                # Para corrigir o valor do hardware ao longo do tempo
                for ano in range(b.ano + 1, self.municipio.tempo_analise):
                    capex_radio_infraesturtura_bs[ano] += capex_radio_infraesturtura_bs[ano - 1] *  \
                                                          (1 + CAPEX.TAXA_DEPRECIACAO.valor)
                capex_radio_infraesturtura += capex_radio_infraesturtura_bs

        return capex_radio_infraesturtura

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
                                                            (1 + OPEX.TAXA_CORRECAO.valor)
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
                                                               (1 + OPEX.TAXA_CORRECAO.valor)

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
            opex_radio_viagens[linha][linha] += self.municipio.tempo_viagem * \
                                                OPEX.QTD_TECNICOS.valor * \
                                                OPEX.SALARIO_TECNICO.valor * \
                                                OPEX.QTD_TIMES.valor * \
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
        opex_radio_penalidades_bs = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))

        for b in lista_bs:
            opex_radio_falhas_bs = np.zeros((self.municipio.tempo_analise, self.municipio.tempo_analise))

            # Determinamos os valores de AFR e MTTR de acordo com o tipo de BS
            if b.tipo_BS.tipo is 'Macro':
                afr = OPEX.TAXA_ARF_MACRO.valor
                mttr = OPEX.MTTR_MACRO.valor
                valor_manutencao = OPEX.MANUTENCAO_MACRO.valor
            elif b.tipo_BS.tipo is 'Micro':
                afr = OPEX.TAXA_ARF_MICRO.valor
                mttr = OPEX.MTTR_MICRO.valor
                valor_manutencao = OPEX.MANUTENCAO_MICRO.valor
            elif b.tipo_BS.tipo is 'Pico':
                afr = OPEX.TAXA_ARF_PICO.valor
                mttr = OPEX.MTTR_PICO.valor
                valor_manutencao = OPEX.MANUTENCAO_PICO.valor
            else:
                afr = OPEX.TAXA_ARF_FEMTO.valor
                mttr = OPEX.MTTR_FEMTO.valor
                valor_manutencao = OPEX.MANUTENCAO_FEMTO.valor

            # Realizar a atualizacao do valor de manutenção corretiva ajustado por ano
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_manutencao_ajustado = util.atualizacao_linear(valor_manutencao,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

            # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
            # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
            valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                     OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                     self.municipio.tempo_analise)

            for linha in range(b.ano, self.municipio.tempo_analise):
                valor_falha = ((mttr + 2.0 * self.municipio.tempo_viagem) *
                               OPEX.QTD_TECNICOS.valor *
                               OPEX.QTD_TIMES.valor *
                               valor_salario_tecnico_ajustado[linha] + valor_manutencao_ajustado[linha]) * afr
                opex_radio_falhas_bs[linha][linha] += valor_falha
                for coluna in range(linha + 1, self.municipio.tempo_analise):
                    # Realiza uma correção financeira no valor para analisá-lo no ano presente
                    opex_radio_falhas_bs[linha][coluna] += opex_radio_falhas_bs[linha][coluna - 1] * \
                                                           (1 + OPEX.TAXA_CORRECAO.valor)
            opex_radio_falhas += opex_radio_falhas_bs.sum(axis=0)

            # Cálculo de Falhas por BS de alta importânica
            # Assumimos 1 BS como sendo de alta importância, por aglomerado
            # Esta BS é a BS marcada como Hub (True)
            if (b.hub_bs is True) and (self.municipio.tempo_medio_disponibilidade < OPEX.THRESHOLD_MACRO.valor):

                # Realizar a atualização do valor de taxa de penalidade por ano
                # Observar o parâmetro alpha da equacao (1.1) de de Yaghoubi et al (2019).
                taxa_penalidade_ajustada = util.atualizacao_linear(OPEX.TAXA_PENALIDADE.valor,
                                                                   OPEX.TAXA_REAJUSTE.valor,
                                                                   self.municipio.tempo_analise)

                for linha in range(b.ano, self.municipio.tempo_analise):
                    valor_penalidade = (OPEX.THRESHOLD_MACRO.valor - self.municipio.tempo_medio_disponibilidade) * \
                                        taxa_penalidade_ajustada[linha]
                    opex_radio_penalidades_bs[linha][linha] += valor_penalidade
                    for coluna in range(linha + 1, self.municipio.tempo_analise):
                        # Realiza uma correção financeira no valor para analisá-lo no ano presente
                        opex_radio_penalidades_bs[linha][coluna] += opex_radio_penalidades_bs[linha][coluna - 1] * \
                                                                    (1 + OPEX.TAXA_CORRECAO.valor)
                opex_radio_falhas += opex_radio_penalidades_bs.sum(axis=0)

        return opex_radio_falhas
