from library.hetnet.AtualizacaoBS import AtualizacaoBS
from library.hetnet.TipoBS import TipoBS


class BS:
    def __init__(self, id_, tipo, ano=0, existenncia_previa=True):
        self.id = id_
        self.tipo_BS = tipo
        self.ano = ano
        self.existencia_previa = existenncia_previa
        self.atualizacoes = list()

    def upgrade(self, ano):
        switcher = {
            TipoBS.MACRO_2G: TipoBS.MACRO_3G,
            TipoBS.MACRO_3G: TipoBS.MACRO_4G,
            TipoBS.MACRO_4G: TipoBS.MACRO_45G,
            TipoBS.MICRO_4G: TipoBS.MICRO_45G,
            TipoBS.PICO_4G: TipoBS.PICO_45G,
            TipoBS.FEMTO_4G: TipoBS.FEMTO_45G,
        }
        atualizacao = switcher.get(self.tipo_BS, False)
        if atualizacao is False:
            return False
        else:
            self.tipo_BS = atualizacao
            self.atualizacoes.append(AtualizacaoBS(atualizacao, ano))
            return True
