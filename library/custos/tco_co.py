import numpy as np

from library.custos.capex import CAPEX
from library.custos.opex import OPEX
from library.custos.tco import TCO
from library.util import util


class TcoCO(TCO):

    def __init__(self, municipio):
        componente = 'CO'
        TCO.__init__(self, municipio, componente)

    def get_capex(self):
        self.municipio.capex_co['equipamentos'], self.municipio.capex_co['instalacao'] = self.get_capex_implantacoes(None, None)
        self.municipio.capex_co['infraestrutura'] = self.get_capex_infraestrutura(None, None)

    def get_opex(self):
        self.municipio.opex_co['energia'] = self.get_opex_energia(None, None)
        self.municipio.opex_co['manutencao'] = self.get_opex_manutencao(None, None)
        self.municipio.opex_co['aluguel'] = self.get_opex_aluguel(None)
        self.municipio.opex_co['falhas'] = self.get_opex_falhas(None, None)

    def get_capex_implantacoes(self, param_1, param_2):
        capex_co_equipamentos = np.zeros(self.municipio.tempo_analise)
        capex_co_instalacao = np.zeros(self.municipio.tempo_analise)

        # Realizar o cálculo de atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(CAPEX.SALARIO_TECNICO.valor,
                                                                 CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        for t, fs in enumerate(self.municipio.co.qtd_fs):
            equipamentos = fs * CAPEX.FS.valor
            equipamentos += self.municipio.co.qtd_as[t] * CAPEX.SW_CARRIER.valor
            tempo_instalacao = fs * 1.0 + self.municipio.co.qtd_as[t] * 0.5

            if equipamentos > 0:
                custo_hardware_ajustado = util.atualizacao_linear(equipamentos,
                                                              CAPEX.TAXA_REAJUSTE.valor,
                                                              self.municipio.tempo_analise)

                capex_co_equipamentos[t] += 0.5 * custo_hardware_ajustado[t]

                # Pagasmento de Salários:
                # Despesas de Instalação relativa ao tempo total de deslocamento e atualização
                despesas_rh = CAPEX.QTD_TECNICOS_INSTALACAO.valor * \
                              CAPEX.QTD_TIMES.valor * \
                              valor_salario_tecnico_ajustado[t] * \
                              (tempo_instalacao + (self.municipio.tempo_viagem * 2.0))

                capex_co_instalacao[t] += 0.5 * despesas_rh

        return capex_co_equipamentos, capex_co_instalacao

    def get_capex_atualizacoes(self, param_1):
        pass

    def get_capex_infraestrutura(self, param_1, param_2):

        # Realizar o cálculo de atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_udc_ajustado = util.atualizacao_linear(CAPEX.UDC.valor,
                                                                 CAPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        capex_co_infraesturtura = 0.5 * np.multiply(self.municipio.co.qtd_udc, valor_udc_ajustado)

        return capex_co_infraesturtura

    def get_opex_energia(self, param_1, param_2):
        opex_co_energia = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula-se a variacao da tarifa de energia ao longo dos anos
        tarifa_energia_ajustada = util.atualizacao_linear(OPEX.CONSUMO.valor,
                                                          OPEX.TAXA_REAJUSTE.valor,
                                                          self.municipio.tempo_analise)
        consumo = np.zeros(self.municipio.tempo_analise)
        for t, fs in enumerate(self.municipio.co.qtd_fs):
            potencia_equipamentos = fs * 0.650 + self.municipio.co.qtd_as[t] * 0.400 + self.municipio.co.qtd_udc[t] * 22.0
            if potencia_equipamentos > 0:
                for t_index in range (t, self.municipio.tempo_analise):
                    consumo[t_index] += potencia_equipamentos * 365.0 * 24.0

        opex_co_energia += 0.5 * np.multiply(consumo, tarifa_energia_ajustada)
        return opex_co_energia

    def get_opex_manutencao(self, param_1, param_2):
        opex_co_manutencao = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        # Realizar a atualizacao do valor de manutenção corretiva ajustado por ano
        valor_manutencao_ps = util.atualizacao_linear(OPEX.MANUTENCAO_PS.valor,
                                                      OPEX.TAXA_REAJUSTE.valor,
                                                      self.municipio.tempo_analise)

        valor_manutencao_udc = util.atualizacao_linear(OPEX.MANUTENCAO_UDC.valor,
                                                       OPEX.TAXA_REAJUSTE.valor,
                                                       self.municipio.tempo_analise)

        valor_manutencao_sw = util.atualizacao_linear(OPEX.MANUTENCAO_SW.valor,
                                                      OPEX.TAXA_REAJUSTE.valor,
                                                      self.municipio.tempo_analise)

        for t, udc in enumerate(self.municipio.co.qtd_udc):
            for t_index in range(t, self.municipio.tempo_analise):
                manut_udc = udc * valor_manutencao_udc[t_index]
                manut_fs = self.municipio.co.qtd_fs[t] * valor_manutencao_ps[t_index]
                manut_as = self.municipio.co.qtd_as[t] * valor_manutencao_sw[t_index]
                opex_co_manutencao[t_index] += manut_udc + manut_fs + manut_as

        tecnicos = OPEX.QTD_TECNICOS.valor * OPEX.QTD_TIMES.valor
        for t, udc in enumerate(self.municipio.co.qtd_udc):
            for t_index in range(t, self.municipio.tempo_analise):
                manut_udc = udc * OPEX.MTTR_PS.valor * tecnicos * valor_salario_tecnico_ajustado[t_index]
                manut_fs = self.municipio.co.qtd_fs[t] * OPEX.MTTR_PS.valor * tecnicos * valor_salario_tecnico_ajustado[t_index]
                manut_as = self.municipio.co.qtd_as[t] * OPEX.MTTR_MW_SW.valor * tecnicos * valor_salario_tecnico_ajustado[t_index]
                opex_co_manutencao[t_index] += manut_udc + manut_fs + manut_as

            opex_co_manutencao[t] += tecnicos * valor_salario_tecnico_ajustado[t] * 2.0 * self.municipio.tempo_viagem

        return opex_co_manutencao

    def get_opex_aluguel(self, param_1):
        opex_co_aluguel = np.zeros(self.municipio.tempo_analise)

        # Primeiro se calcula a variacao do preco de alguel por m2 ao longo dos anos
        aluguel_area_outdoor_ajustado = util.atualizacao_linear(OPEX.ALUGUEL_OUTDOOR.valor,
                                                                OPEX.TAXA_REAJUSTE.valor,
                                                                self.municipio.tempo_analise)

        area_total = np.zeros(self.municipio.tempo_analise)
        for t, udc in enumerate(self.municipio.co.qtd_udc):
            area_udc = udc * 14.98
            if area_udc > 0:
                for t_index in range(t, self.municipio.tempo_analise):
                    area_total[t_index] += area_udc

        opex_co_aluguel += 0.5 * np.multiply(area_total, aluguel_area_outdoor_ajustado)

        return opex_co_aluguel

    def get_opex_falhas(self, param_1, param_2):
        opex_co_falhas = np.zeros(self.municipio.tempo_analise)

        # Realizar a atualização do valor de salário do técnico de manutenção ajustado por ano
        valor_salario_tecnico_ajustado = util.atualizacao_linear(OPEX.SALARIO_TECNICO.valor,
                                                                 OPEX.TAXA_CORRECAO_SALARARIO.valor,
                                                                 self.municipio.tempo_analise)

        afr = OPEX.TAXA_ARF_PS.valor
        mttr = OPEX.MTTR_PS.valor + OPEX.MTTR_UDC.valor + OPEX.MTTR_MW_SW.valor

        # Realizar a atualizacao do valor de manutenção corretiva ajustado por ano
        valor_manutencao_ps = util.atualizacao_linear(OPEX.MANUTENCAO_PS.valor,
                                                      OPEX.TAXA_REAJUSTE.valor,
                                                      self.municipio.tempo_analise)

        valor_manutencao_udc = util.atualizacao_linear(OPEX.MANUTENCAO_UDC.valor,
                                                       OPEX.TAXA_REAJUSTE.valor,
                                                       self.municipio.tempo_analise)

        valor_manutencao_sw = util.atualizacao_linear(OPEX.MANUTENCAO_SW.valor,
                                                      OPEX.TAXA_REAJUSTE.valor,
                                                      self.municipio.tempo_analise)

        for t, udc in enumerate(self.municipio.co.qtd_udc):
            opex_co_falhas[t] += ((mttr + 2.0 * self.municipio.tempo_viagem) *
                                  OPEX.QTD_TECNICOS.valor *
                                  OPEX.QTD_TIMES.valor *
                                  valor_salario_tecnico_ajustado[t] + valor_manutencao_ps[t] + valor_manutencao_udc[t] +
                                  valor_manutencao_sw[t]) * \
                                 afr

        return opex_co_falhas
