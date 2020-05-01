from library.hetnet.AtualizacaoBS import AtualizacaoBS
from library.hetnet.BSType import BSType
from library.hetnet.TipoAtualizacaoBS import TipoAtualizacaoBS


class BS:
    def __init__(self, id_, tipo, ano=0, existenncia_previa=True):
        self.id = id_
        self.tipo_BS = tipo
        self.ano = ano
        self.existencia_previa = existenncia_previa
        self.atualizacoes = list()

    def upgrade(self, ano):
        if self.tipo_BS.atualizavel is True:
            if self.tipo_BS.ambiente == 'outdoor':
                if self.tipo_BS.tecnologia == '2G':
                    self.tipo_BS = BSType.MACRO_3G
                    self.atualizacoes.append(AtualizacaoBS(TipoAtualizacaoBS.PARA_3G, ano))
                    return True
                else:
                    if self.tipo_BS.tecnologia == '3G':
                        self.tipo_BS = BSType.MACRO_4G
                        self.atualizacoes.append(AtualizacaoBS(TipoAtualizacaoBS.PARA_4G, ano))
                        return True
                    else:
                        if self.tipo_BS.tecnologia == '4G':
                            self.tipo_BS = BSType.MACRO_5G
                            self.atualizacoes.append(AtualizacaoBS(TipoAtualizacaoBS.PARA_5G, ano))
                            return True
                        else:
                            return False
            else:
                if self.tipo_BS.tecnologia == '4G':
                    self.tipo_BS = BSType.FEMTO_5G
                    self.atualizacoes.append(AtualizacaoBS(TipoAtualizacaoBS.PARA_5G, ano))
                    return True
                else:
                    return False
        else:
            return False
