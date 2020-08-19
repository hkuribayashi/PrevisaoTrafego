from enum import Enum


class CF(Enum):

    TAXA_SUBSCRICAO_GOV = ('Taxa Mensal de Subscrição de Terminal', '$/terminal', 0.00003635454545)
    # TAXA_SUBSCRICAO_GOV = ('Taxa Mensal de Subscrição de Terminal', '$/terminal', 0.00001817727273)

    TAXA_SUBSCRICAO_USUARIO = ('Taxa Mensal de Subscrição de Terminal', '$/terminal', 0.00007270909091)

    TAXA_DESCONTO = ('Taxa de Desconto', '%', 0.1)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "CF descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)
