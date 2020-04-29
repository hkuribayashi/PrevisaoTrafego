from enum import Enum


class BSType(Enum):
    MACRO_2G = ('Macro', '2G', 'outdoor', 3.0, 5.0, True)
    MACRO_3G = ('Macro', '3G', 'outdoor', 3.0, 45.0, True)
    MACRO_4G = ('Macro', '4G', 'outdoor', 3.0, 168.0, True)
    FEMTO_4G = ('Femto', '4G', 'indoor', 1.0, 168.0, True)
    MACRO_5G = ('Macro', '5G', 'outdoor', 3.0, 1132.0, False)
    FEMTO_5G = ('Femto', '5G', 'indoor', 1.0, 1132.0, False)

    def __init__(self, tipo, tecnologia, ambiente, setores, capacidade, atualizavel):
        self.tipo = tipo
        self.tecnologia = tecnologia
        self.ambiente = ambiente
        self.setores = setores
        self.capacidade = capacidade
        self.atualizavel = atualizavel
