from enum import Enum


class CF(Enum):

    TAXA_SUBSCRICAO = ('Taxa Mensal de Subscrição de Terminal', '$/terminal', 0.00005454545455)
    TAXA_DESCONTO = ('Taxa de Desconto', '%', 0.1)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "CF descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)
