import math


class Ponto:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distancia_euclidiana(self, outro_ponto):
        return math.sqrt((self.x - outro_ponto.x) ** 2 + (self.y - outro_ponto.y) ** 2)

    def get_distancia_manhattan(self, outro_ponto):
        return abs(self.x - outro_ponto.x) + abs(self.y - outro_ponto.y)

    def __str__(self):
        return '({},{})'.format(self.x, self.y)