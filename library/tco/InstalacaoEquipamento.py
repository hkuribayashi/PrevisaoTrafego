from enum import Enum


class InstalacaoEquipamento(Enum):
    DESLOCAMENTO = ('Tempo de Deslocamento para o Aglomerado', 1.0, 'horas/trecho')
    G_ETHERNET_SWITCH = ('Tempo de Instalação G-Ethernet Switch', 1.0, 'horas/switch')
    ETHERNET_SWITCH = ('Tempo de Instalação Ethernet Switch', 1.0, 'horas/switch')
    TECNICO = ('Salário do Técnico de Instalação', 1.0, '$/hora')

    def __init__(self, nome, tempo, unidade, quantidade_tecnicos=2):
        self.nome = nome
        self.tempo = tempo
        self.unidade = unidade
        self.quantidade_tecnicos = quantidade_tecnicos


class InstalacaoEquipamentoFibra(InstalacaoEquipamento):

    FIBRA = ('Tempo para dividir e conectar cada fibra ótica', 1.0, 'horas/fibra')

    ONU = ('Tempo de Instalação Modem ONU', 1.0, 'horas/ONU')
    OLT = ('Tempo de Instalação OLT', 1.0, 'horas/OLT')
    SPLITTER_16 = ('Tempo de Instalação Power splitter 1:16', 1.0, 'horas/splitter')
    SPLITTER_32 = ('Tempo de Instalação Power splitter 1:32', 1.0, 'horas/splitter')

    def __init__(self, nome, tempo, unidade, quantidade_tecnicos=2):
        super().__init__(nome, tempo, unidade, quantidade_tecnicos)


class InstalacaoEquipamentoMW(InstalacaoEquipamento):

    MW = ('Tempo para instalar uma Antena de MW', 1.0, 'horas/antenna')

    def __init__(self, nome, tempo, unidade, quantidade_tecnicos=2):
        super().__init__(nome, tempo, unidade, quantidade_tecnicos)
