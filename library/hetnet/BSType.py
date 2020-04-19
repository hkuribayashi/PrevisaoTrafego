from enum import Enum


class BSType(Enum):
    MACRO_2G = ('2G', 'outdoor', 20.0, 3.0, 5.0)
    MACRO_3G = ('3G', 'outdoor', 10.0, 3.0, 45.0)
    MACRO_4G = ('4G', 'outdoor', 1.0211, 3.0, 168.0)
    FEMTO_4G = ('4G', 'indoor', 0.0013, 1.0, 168.0)
    MACRO_5G = ('5G', 'outdoor', '0.0313', 3.0, 3396.0)
    FEMTO_5G = ('5G', 'indoor', '0.0013', 3.0, 3396.0)

    def __init__(self, tecnologia, ambiente, cobertura, setores, capacidade):
        self._tecnologia = tecnologia
        self._ambiente = ambiente
        self._cobertura = cobertura
        self._setores = setores
        self._capacidade = capacidade

    @property
    def tecnologia(self):
        return self._tecnologia

    @property
    def ambiente(self):
        return self._ambiente

    @property
    def cobertura(self):
        return self._cobertura

    @property
    def setores(self):
        return self._setores

    @property
    def capacidade(self):
        return self._capacidade
