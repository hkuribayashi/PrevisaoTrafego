from library.hetnet.AtualizacaoBS import AtualizacaoBS
from library.hetnet.BSType import BSType


class BS:
    def __init__(self, id_, operadora, tipo, existenncia_previa=True):
        self._id = id_
        self._operadora = operadora
        self._tipo_BS = tipo
        self._existencia_previa = existenncia_previa
        self._atualizacoes = list()

    @property
    def id(self):
        return self._id

    @property
    def operadora(self):
        return self._operadora

    @property
    def tipo_BS(self):
        return self._tipo_BS

    @property
    def existencia_previa(self):
        return self._existencia_previa

    @id.setter
    def id(self, id_):
        if id_ is None:
            raise RuntimeError('[ERROR]')
        else:
            self._id = id_

    @operadora.setter
    def operadora(self, operadora):
        if operadora is None:
            raise RuntimeError('[ERROR]')
        else:
            self._operadora = operadora

    @tipo_BS.setter
    def tipo_BS(self, tipo):
        if tipo is None:
            raise RuntimeError('[ERROR]')
        else:
            self._tipo_BS = tipo

    @existencia_previa.setter
    def existencia_previa(self, existencia_previa):
        self._existencia_previa = existencia_previa

    def upgrade(self):
        if self._tipo_BS.atualizavel is True:
            if self._tipo_BS.ambiente == 'outdoor':
                if self._tipo_BS.tecnologia == '2G':
                    self._tipo_BS = BSType.MACRO_3G
                    self._atualizacoes.append(AtualizacaoBS.ATUALIZACAO_2G_PARA_3G)
                else:
                    if self._tipo_BS.tecnologia == '3G':
                        self._tipo_BS = BSType.MACRO_4G
                        self._atualizacoes.append(AtualizacaoBS.ATUALIZACAO_3G_PARA_4G)
                    else:
                        if self._tipo_BS.tecnologia == '4G':
                            self._tipo_BS = BSType.MACRO_5G
                            self._atualizacoes.append(AtualizacaoBS.ATUALIZACAO_4G_PARA_5G)
            else:
                if self._tipo_BS.tecnologia == '4G':
                    self._tipo_BS = BSType.FEMTO_5G
                    self._atualizacoes.append(AtualizacaoBS.ATUALIZACAO_4G_PARA_5G)
            return True
        else:
            return False
