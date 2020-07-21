from enum import Enum


class PARAM(Enum):

    DIRETORIO_IMAGEM = ('Diretório Export Gráficos', 'diretorio', '/Users/hugo/Desktop/')
    RESOLUCAO_IMAGEM = ('Resolução Export Gráficos', 'dpi', 600)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "Param descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)
