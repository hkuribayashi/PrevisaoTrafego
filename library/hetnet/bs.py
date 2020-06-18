from library.hetnet.atualizacao_bs import AtualizacaoBS
from library.hetnet.tipo_bs import TipoBS


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

    '''
    Este método foi criado para evitar que se contabilizem duas atualizações de BS no mesmo ano
    Não sei se não seria melhor utilizar ao invés da list uma outra estrutura que não permitisse elementos duplicados,
    porém esta questão fica para uma melhoria futura. 
    '''
    def ajuste_atualizacoesBS(self):
        lista_ajustada = list()
        ultimo_ano = -1
        for at in self.atualizacoes:
            if at.ano != ultimo_ano:
                ultimo_ano = at.ano
                lista_ajustada.append(at)
            else:
                lista_ajustada[-1] = at
        self.atualizacoes = lista_ajustada

    def __str__(self):
        return "id={}, tipo={}, ano={}, ponto={}, hub_bs={}, existencia_previa={}".format(self.id, self.tipo_BS,
                                                                                          self.ano, self.ponto,
                                                                                          self.hub_bs,
                                                                                          self.existencia_previa)
