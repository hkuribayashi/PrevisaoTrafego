from library.entities import Aglomerado
from library.hetnet import BS, Operadora, TipoBS


a1 = Aglomerado(100.0, 100.0, 15, 0.9, 60, 40, 20, 10, 10, 0.8, 0.45, 0.95, 0.45, 0.16)
b1 = BS(1, Operadora.operadora1, TipoBS.MACRO_2G, a1)

b1.upgrade()
print(b1.tipo_BS)