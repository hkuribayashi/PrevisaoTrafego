from enum import Enum


class Energia(Enum):

    CONSUMO = ('Tarifa de Consumo de kWh', '$/kWh', 0.1)
    VENDA = ('Tarifa de Consumo de kWh', '$/kWh', 0.1)

    def __init__(self, descricao, unidade, valor):
        self.descricao = descricao
        self.unidade = unidade
        self.valor = valor

    def __str__(self):
        return "Energia descricao={}, unidade={}, valor={}".format(self.descricao, self.unidade, self.valor)
