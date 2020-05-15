from library.hetnet.AtualizacaoBS import AtualizacaoBS
from library.hetnet.TipoBS import TipoBS


class BS:
    def __init__(self, id_, tipo, ponto, ano=0, hub_bs=False, existenncia_previa=False):
        self.id = id_
        self.tipo_BS = tipo
        self.ponto = ponto
        self.ano = ano
        self.hub_bs = hub_bs
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

    def __str__(self):
        return "id={}, tipo={}, ano={}, ponto={}, hub_bs={}, existencia_previa={}".format(self.id, self.tipo_BS,
                                                                                          self.ano, self.ponto,
                                                                                          self.hub_bs,
                                                                                          self.existencia_previa)
