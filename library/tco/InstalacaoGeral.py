from enum import Enum


'''
Esta classe deve ajudar o dimensionamento de despesas de instalação de equipamentos
Em ambos os casos da implantação, tais despesas são relativas ao custo de instalação dos equipamentos envolvidos
'''


class Instalacao(Enum):

    def __init__(self, nome, preco_unitario, unidade_medida, quantidade_tecnicos=2):
        self.nome = nome
        self.preco_unitario = preco_unitario
        self.unidade_medida = unidade_medida
        self.quantidade_tecnicos = quantidade_tecnicos


class InstalacaoGeral(Instalacao):

    #Despesas de deslocamemento devem ser alteradas conforme o município
    DESLOCAMENTO = ('Tempo de Deslocamento para o Aglomerado', 18.0, 'horas/trecho')
    G_ETHERNET_SWITCH = ('Tempo de Instalação G-Ethernet Switch', 1.0, 'horas/switch')
    ETHERNET_SWITCH = ('Tempo de Instalação Ethernet Switch', 1.0, 'horas/switch')
    TECNICO = ('Salário do Técnico de Instalação', 10.0, '$/hora')

    def __init__(self, nome, preco_unitario, unidade_medida, quantidade_tecnicos=2):
        super().__init__(nome, preco_unitario, unidade_medida, quantidade_tecnicos)


class InstalacaoRadio(Instalacao):

    MACRO = ('Custo de Instalação de Macro BS', 1000.0, '$/unidade')
    MICRO = ('Custo de Instalação de Micro BS', 1000.0, '$/unidade')
    SBS = ('Custo de Instalação de SBS', 200.0, '$/unidade')

    ATUALIZACAO_MACRO = ('Custo de Instalação de Atualização de MBS', 100.0, '$/unidade')
    ATUALIZACAO_SMALL = ('Custo de Instalação de Atualização de SBS', 100.0, '$/unidade')

    def __init__(self, nome, preco_unitario, unidade_medida, quantidade_tecnicos=2):
        super().__init__(nome, preco_unitario, unidade_medida, quantidade_tecnicos)


class InstalacaoEquipamentoFibra(Instalacao):

    FIBRA = ('Tempo para dividir e conectar cada fibra ótica', 1.0, 'horas/fibra')

    ONU = ('Tempo de Instalação Modem ONU', 1.0, 'horas/ONU')
    OLT = ('Tempo de Instalação OLT', 1.0, 'horas/OLT')
    SPLITTER_16 = ('Tempo de Instalação Power splitter 1:16', 1.0, 'horas/splitter')
    SPLITTER_32 = ('Tempo de Instalação Power splitter 1:32', 1.0, 'horas/splitter')

    def __init__(self, nome, preco_unitario, unidade_medida, quantidade_tecnicos=2):
        super().__init__(nome, preco_unitario, unidade_medida, quantidade_tecnicos)


class InstalacaoEquipamentoMW(Instalacao):

    MW = ('Tempo para instalar uma Antena de MW', 1.0, 'horas/antenna')

    def __init__(self, nome, preco_unitario, unidade_medida, quantidade_tecnicos=2):
        super().__init__(nome, preco_unitario, unidade_medida, quantidade_tecnicos)
