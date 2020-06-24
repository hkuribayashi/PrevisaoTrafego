from enum import Enum


class OPEX(Enum):

    # Despesas de Energia
    CONSUMO = ('Tarifa de Consumo de kWh', '$/kWh', 0.00000113)
    VENDA = ('Tarifa de Consumo de kWh', '$/kWh', 0.00000113)

    # Reajuste anual de Preços
    TAXA_REAJUSTE = ('Taxa de reajuste de despesas', '%/ano', 0.03)

    # Correção Monetária
    TAXA_CORRECAO = ('Taxa de correção monetária', '%/ano', 0.005)

    # Despesas de Aluguel
    ALUGUEL_OUTDOOR = ('Valor de aluguel anual por m2 outdoor', '$/m2', 0.0018)
    ALUGUEL_INDOOR = ('Valor de aluguel anual por m2 indoor', '$/m2', 0.0022)

    # Despesas de Manutenção de BSs
    MANUTENCAO_MACRO_2G = ('Valor de manutencao anual por Macro BS 2G', '$/BS', 0.0038)
    MANUTENCAO_MACRO_3G = ('Valor de manutencao anual por Macro BS 3G', '$/BS', 0.0038)
    MANUTENCAO_MACRO_4G = ('Valor de manutencao anual por Macro BS 4G', '$/BS', 0.0042)
    MANUTENCAO_MACRO_45G = ('Valor de manutencao anual por Macro BS 4.5G', '$/BS', 0.0046)
    MANUTENCAO_MACRO_5G = ('Valor de manutencao anual por Macro BS 5G', '$/BS', 0.0048)

    MANUTENCAO_MICRO_3G = ('Valor de manutencao anual por Micro BS 3G', '$/BS', 0.00057)
    MANUTENCAO_MICRO_4G = ('Valor de manutencao anual por Micro BS 4G', '$/BS', 0.00063)
    MANUTENCAO_MICRO_45G = ('Valor de manutencao anual por Micro BS 4.5G', '$/BS', 0.00069)
    MANUTENCAO_MICRO_5G = ('Valor de manutencao anual por Micro BS 5G', '$/BS', 0.00072)

    MANUTENCAO_FEMTO_4G = ('Valor de manutencao anual por Femto BS 4G', '$/BS', 0.0001)
    MANUTENCAO_FEMTO_45G = ('Valor de manutencao anual por Femto BS 4.5G', '$/BS', 0.0001)
    MANUTENCAO_FEMTO_5G = ('Valor de manutencao anual por Femto BS 5G', '$/BS', 0.0001)

    # Despesas de Manutenção relacionada a RH
    SALARIO_TECNICO = ('Salário do Técnico de Manutenção', '$/hora', 0.00052)
    QTD_TECNICOS = ('Qtd de Técnicos por Time', 'técnicos/time', 1.0)
    QTD_TIMES = ('Quantidade de times', 'times/manutenção', 1.0)
    TAXA_CORRECAO_SALARARIO = ('Taxa de Correção de Salário do Técnico de Manutenção', '%/ano', 0.05)

    # Taxas Anual de Falhas
    TAXA_ARF_MACRO = ('Taxa Anual de Falha Macro BS', 'taxa', 0.0584)
    TAXA_ARF_MICRO = ('Taxa Anual de Falha Micro BS', 'taxa', 0.0584)
    TAXA_ARF_PICO = ('Taxa Anual de Falha Pico BS', 'taxa', 0.0584)
    TAXA_ARF_FEMTO = ('Taxa Anual de Falha Femto BS', 'taxa', 0.0584)

    # Tempo médio de reparos
    MTTR_MACRO = ('Tempo Médio de Reparo de Macro BS', 'horas/bs', 1.0)
    MTTR_MICRO = ('Tempo Médio de Reparo de Micro BS', 'horas/bs', 1.0)
    MTTR_PICO = ('Tempo Médio de Reparo de Pico BS', 'horas/bs', 0.2)
    MTTR_FEMTO = ('Tempo Médio de Reparo de Femto BS', 'horas/bs', 0.2)

    # Penalidades
    THRESHOLD_MACRO = ('Tempo Mínimo de Funcionamento por Ano', 'horas/ano', 8322.0)
    TAXA_PENALIDADE = ('Taxa de Penalidade por Indiponibilidade', '$/hora', 0.01)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "OPEX descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)

