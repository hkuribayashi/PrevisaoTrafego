from library.hetnet.AtualizacaoBS import AtualizacaoBS
from library.hetnet.BSType import BSType


class BS:
    def __init__(self, id_, tipo, existenncia_previa=True):
        self.id = id_
        self.tipo_BS = tipo
        self.existencia_previa = existenncia_previa
        self.atualizacoes = list()

    def upgrade(self):
        if self.tipo_BS.atualizavel is True:
            if self.tipo_BS.ambiente == 'outdoor':
                if self.tipo_BS.tecnologia == '2G':
                    self.tipo_BS = BSType.MACRO_3G
                    self.atualizacoes.append(AtualizacaoBS.ATUALIZACAO_2G_PARA_3G)
                    return True
                else:
                    if self.tipo_BS.tecnologia == '3G':
                        self.tipo_BS = BSType.MACRO_4G
                        self.atualizacoes.append(AtualizacaoBS.ATUALIZACAO_3G_PARA_4G)
                        return True
                    else:
                        if self.tipo_BS.tecnologia == '4G':
                            self.tipo_BS = BSType.MACRO_5G
                            self.atualizacoes.append(AtualizacaoBS.ATUALIZACAO_4G_PARA_5G)
                            return True
                        else:
                            return False
            else:
                if self.tipo_BS.tecnologia == '4G':
                    self.tipo_BS = BSType.FEMTO_5G
                    self.atualizacoes.append(AtualizacaoBS.ATUALIZACAO_4G_PARA_5G)
                    return True
                else:
                    return False
        else:
            return False
