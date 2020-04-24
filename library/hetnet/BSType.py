from enum import Enum


class BSType(Enum):
    MACRO_2G = ('2G', 'outdoor', 20.0, 3.0, 5.0, True)
    MACRO_3G = ('3G', 'outdoor', 10.0, 3.0, 45.0, True)
    MACRO_4G = ('4G', 'outdoor', 1.0211, 3.0, 168.0, True)
    FEMTO_4G = ('4G', 'indoor', 0.0013, 1.0, 168.0, True)
    MACRO_5G = ('5G', 'outdoor', 0.0313, 3.0, 3396.0, False)
    FEMTO_5G = ('5G', 'indoor', 0.0013, 3.0, 3396.0, False)

    def __init__(self, tecnologia, ambiente, cobertura, setores, capacidade, atualizavel):
        self.tecnologia = tecnologia
        self.ambiente = ambiente
        self.cobertura = cobertura
        self.setores = setores
        self.capacidade = capacidade
        self.atualizavel = atualizavel
