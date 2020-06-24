from enum import Enum


class TipoBS(Enum):
    MACRO_2G = ('Macro', '2G', 'outdoor', 3.0, 5.0, 10.0, 39.81, 100.0, True)
    MACRO_3G = ('Macro', '3G', 'outdoor', 3.0, 45.0, 3.33, 39.81, 100.0, True)
    MACRO_4G = ('Macro', '4G', 'outdoor', 3.0, 76.0, 1.02, 39.81, 100.0, True)
    MACRO_45G = ('Macro', '4.5G', 'outdoor', 3.0, 168.0, 1.02, 39.81, 100.0, False)
    MACRO_5G = ('Macro', '5G', 'outdoor', 3.0, 1132.0, 0.0314, 39.81, 100.0, False)

    MICRO_4G = ('Micro', '4G', 'outdoor', 3.0, 76.0, 0.51, 1.0, 100.0, True)
    MICRO_45G = ('Micro', '4.5G', 'outdoor', 3.0, 168.0, 0.51, 1.0, 100.0, False)
    MICRO_5G = ('Micro', '5G', 'outdoor', 3.0, 1132.0, 0.0157, 1.0, 100.0, False)

    FEMTO_4G = ('Femto', '4G', 'indoor', 1.0, 132.0, 0.008, 0.1, 1.0, True)
    FEMTO_45G = ('Femto', '4.5G', 'indoor', 1.0, 291.78, 0.008, 0.1, 1.0, False)
    FEMTO_5G = ('Femto', '5G', 'indoor', 1.0, 1132.0, 0.0013, 0.1, 1.0, False)

    def __init__(self, tipo, tecnologia, ambiente, setores, capacidade, cobertura_por_setor,
                 potencia_transmissao, area_fisica, atualizavel):
        self.tipo = tipo
        self.tecnologia = tecnologia
        self.ambiente = ambiente
        self.setores = setores
        self.capacidade = capacidade
        self.cobertura_por_setor = cobertura_por_setor
        self.potencia_transmissao = potencia_transmissao
        self.area_fisica = area_fisica
        self.atualizavel = atualizavel

    def __str__(self):
        return "TipoBS tipo={}, tec={}".format(self.tipo, self.tecnologia)
