

class AtualizacaoBS():

    def __init__(self, tipo, ano):
        self.tipo = tipo
        self.ano = ano

    def __str__(self):
        return "AtualizacaoBS tipo={}, ano={}".format(self.tipo, self.ano)
