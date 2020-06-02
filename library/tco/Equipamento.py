from enum import Enum

from library.hetnet.TipoBS import TipoBS


class Equipamento(Enum):

    ONU = ('Modem ONU', 150.0, '$/onu')
    OLT = ('4x10G array trahsceiver', 7000.0, '$/unidade')
    SPLITTER_16 = ('Power splitter 1:16', 170.0, '$/unidade')
    SPLITTER_32 = ('Power splitter 1:32', 340.0, '$/unidade')

    ETHERNET_SWITCH = ('Switch Ethernet', 150.0, '$/switch')
    G_ETHERNET_SWITCH = ('G-Ethernet Switch', 1800.0, '$/switch')

    ANTENA_MW_SMALL = ('Antena MW dentro Aglomerado', 500.0, '$/unidade')
    ANTENA_MW_LARGE = ('Antena MW entre Aglomerados', 2000.0, '$/unidade')
    MW_HUB = ('Microwave Hub + instalação', 20000.0, '$/hub')

    MBS = ('Macro Base Station e Cell Site', 48000.0, '$/unidade')
    SBS = ('Small indoor Base Station', 250.0, '$/unidade, 0.03')

    def __init__(self, nome, preco_unitario, unidade_precificacao, desconto=0.03):
        self.nome = nome
        self.preco_unitario = preco_unitario
        self.unidade_precificacao = unidade_precificacao
        self.desconto = desconto

    @staticmethod
    def get_preco_atualizacao(tipo_atualizacaoBS):
        switcher = {
            'MACRO_3G': 2000.0,
            'MACRO_4G': 2000.0,
            'MACRO_45G': 2000.0,
            'MICRO_45G': 20000.0
        }
        return switcher.get(tipo_atualizacaoBS.name, -99.0)

    def __str__(self):
        return 'Equipamento nome={}, preco_unitario={}, unidade_precificacao={}, desconto={}'.format(self.nome, self.preco_unitario, self.unidade_precificacao, self.desconto)
