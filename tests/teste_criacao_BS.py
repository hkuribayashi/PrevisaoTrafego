from library.entities import aglomerado
from library.hetnet import bs, Operadora, tipo_bs


a1 = aglomerado(100.0, 100.0, 15, 0.9, 60, 40, 20, 10, 10, 0.8, 0.45, 0.95, 0.45, 0.16)
b1 = bs(1, Operadora.operadora1, tipo_bs.MACRO_2G, a1)

b1.upgrade()
print(b1.tipo_BS)