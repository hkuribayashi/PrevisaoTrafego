from enum import Enum


class Aluguel(Enum):

    OUTDOOR = ('Valor de aluguel anual por m2 outdoor', '$/m2', 180.0)
    INDOOR = ('Valor de aluguel anual por m2 indoor', '$/m2', 220.0)

    def __init__(self, descricao, unidade, valor):
        self.descricao = descricao
        self.unidade = unidade
        self.valor = valor

    def __str__(self):
        return "Energia descricao={}, unidade={}, valor={}".format(self.descricao, self.unidade, self.valor)
