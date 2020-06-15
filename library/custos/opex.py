from enum import Enum


class OPEX(Enum):

    # Despesas de Energia
    CONSUMO = ('Tarifa de Consumo de kWh', '$/kWh', 0.1)
    VENDA = ('Tarifa de Consumo de kWh', '$/kWh', 0.1)

    # Reajuste anual de Preços
    TAXA_REAJUSTE = ('Taxa de reajuste de despesas', '%/ano', 0.03)

    # Correção Monetária
    TAXA_CORRECAO = ('Taxa de correção monetária', '%/ano', 0.005)

    # Despesas de Aluguel
    ALUGUEL_OUTDOOR = ('Valor de aluguel anual por m2 outdoor', '$/m2', 180.0)
    ALUGUEL_INDOOR = ('Valor de aluguel anual por m2 indoor', '$/m2', 220.0)

    # Despesas de Manutenção de BSs
    MANUTENCAO_MACRO = ('Valor de manutencao anual por Macro BS', '$/BS', 1.0)
    MANUTENCAO_MICRO = ('Valor de manutencao anual por Micro BS', '$/BS', 1.0)
    MANUTENCAO_PICO = ('Valor de manutencao anual por Pico BS', '$/BS', 1.0)
    MANUTENCAO_FEMTO = ('Valor de manutencao anual por Femto BS', '$/BS', 1.0)

    # Despesas de Manutenção relacionada a RH
    DESLOCAMENTO = ('Tempo de Médio de deslocamento para o Aglomerado', 'horas/trecho', 18.0)
    SALARIO_TECNICO = ('Salário do Técnico de Manutenção', '$/hora', 10.0)
    QTD_TECNICOS = ('Qtd de Técnicos por Time', 'técnicos/time', 1.0)
    QTD_TIMES = ('Quantidade de times', 'times/manutenção', 1.0)
    TAXA_CORRECAO_SALARARIO = ('Taxa de Correção de Salário do Técnico de Manutenção', '%/ano', 0.05)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "OPEX descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)

