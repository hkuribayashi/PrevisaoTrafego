from enum import Enum

'''
Esta classe deve ajudar o dimensionamento de despesas de infraestrutura prévia, necessária à instalação dos equipamentos
No caso da implantação por Fibra Ótica tais despesas são relativas ao lançamento de fibra ótica áerea ou subterrânea.
No caso de microwave estas despesas são relativas à implantação de Hubs MW, mastos etc.
'''


class InfraEquipamento(Enum):

    def __init__(self, nome, preco_unitario, unidade_precificacao):
        self.nome = nome
        self.preco_unitario = preco_unitario
        self.unidade_precificacao = unidade_precificacao

    def __str__(self):
        return "Infraestrutura nome={}, preco_unitario={}, unidade_precificacao={}".format(
            self.nome, self.preco_unitario, self.unidade_precificacao)


class InfraRadio(InfraEquipamento):

    TORRE_MACRO = ('Despesas de Implantação de Torre Macro Cell', 100.0, '$/torre')
    TORRE_MICRO = ('Despesas de Implantação de Torre Micro Cell', 100.0, '$/torre')
    TORRE_SMALL = ('Despesas de Implantação de Torre Macro Cell', 0.0, '$/torre')

    def __init__(self, nome, preco_unitario, unidade_precificacao):
        super().__init__(nome, preco_unitario, unidade_precificacao)


class InfraFibra(InfraEquipamento):

    FIBRA_AEREA = ('Implantação Fibra Ótica Aérea (Posteada)', 80.0, '$/km')
    FIBRA_SUBTERRANEA = ('Implantação Fibra Ótica Aérea (Posteada)', 80.0, '$/km')

    def __init__(self, nome, preco_unitario, unidade_precificacao):
        super().__init__(nome, preco_unitario, unidade_precificacao)


class InfraMW(InfraEquipamento):

    MW_HUB = ('Implantação de Hub MW', 1.0, '$/hub')

    def __init__(self, nome, preco_unitario, unidade_precificacao):
        super().__init__(nome, preco_unitario, unidade_precificacao)