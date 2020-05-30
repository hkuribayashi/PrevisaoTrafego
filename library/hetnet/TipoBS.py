from enum import Enum


class TipoBS(Enum):
    MACRO_2G = ('Macro', '2G', 'outdoor', 3.0, 5.0, 10.0, True)
    MACRO_3G = ('Macro', '3G', 'outdoor', 3.0, 45.0, 3.33, True)

    MACRO_4G = ('Macro', '4G', 'outdoor', 3.0, 76.0, 1.02, True)
    MICRO_4G = ('Micro', '4G', 'outdoor', 3.0, 76.0, 0.51, True)
    PICO_4G = ('Pico', '4G', 'indoor', 1.0, 132.0, 0.03, True)
    FEMTO_4G = ('Femto', '4G', 'indoor', 1.0, 132.0, 0.008, True)

    MACRO_45G = ('Macro', '4.5G', 'outdoor', 3.0, 168.0, 1.02, False)
    MICRO_45G = ('Micro', '4.5G', 'outdoor', 3.0, 168.0, 0.51, False)
    PICO_45G = ('Pico', '4.5G', 'indoor', 1.0, 291.78, 0.03, False)
    FEMTO_45G = ('Femto', '4.5G', 'indoor', 1.0, 291.78, 0.008, False)

    MACRO_5G = ('Macro', '5G', 'outdoor', 3.0, 1132.0, 0.0314, False)
    MICRO_5G = ('Micro', '5G', 'outdoor', 3.0, 1132.0, 0.0157, False)
    PICO_5G = ('Pico', '5G', 'indoor', 1.0, 1132.0, 0.013, False)
    FEMTO_5G = ('Femto', '5G', 'indoor', 1.0, 1132.0, 0.0013, False)

    def __init__(self, tipo, tecnologia, ambiente, setores, capacidade, cobertura_por_setor, atualizavel):
        self.tipo = tipo
        self.tecnologia = tecnologia
        self.ambiente = ambiente
        self.setores = setores
        self.capacidade = capacidade
        self.atualizavel = atualizavel
        self.cobertura_por_setor = cobertura_por_setor

    def __str__(self):
        return "TipoBS tipo={}, tec={}".format(self.tipo, self.tecnologia)
