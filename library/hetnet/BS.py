from library.hetnet.BSType import BSType


class BS:
    def __init__(self, id_, operadora, tipo, agrupamento, ):
        self._id = id_
        self._operadora = operadora
        self._tipo_BS = tipo
        self._agrupamento = agrupamento

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
    def agrupamento(self):
        return self._agrupamento

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

    @agrupamento.setter
    def agrupamento(self, agrupamento):
        if agrupamento is None:
            raise RuntimeError('[ERROR]')
        else:
            self._agrupamento = agrupamento

    def upgrade(self):
        if self._tipo_BS.atualizavel is True:
            if self._tipo_BS.ambiente == 'outdoor':
                if self._tipo_BS.tecnologia == '2G':
                    self._tipo_BS = BSType.MACRO_3G
                else:
                    if self._tipo_BS.tecnologia == '3G':
                        self._tipo_BS = BSType.MACRO_4G
                    else:
                        if self._tipo_BS.tecnologia == '4G':
                            self._tipo_BS = BSType.MACRO_5G
            else:
                if self._tipo_BS.tecnologia == '4G':
                    self._tipo_BS = BSType.FEMTO_5G
            return True
        else:
            return False
