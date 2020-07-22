import copy

from library.core.engine import Engine
from library.entities.aglomerado import Aglomerado
from library.entities.municipio import Municipio
from library.entities.ponto import Ponto
from library.hetnet.bs import BS
from library.hetnet.tipo_bs import TipoBS

# Criando um município a partir dos dados de Faro
m1 = Municipio(1, 3272.0, 0.243, 164.0, 0.56, 489.0, 234.0, 134.0, 15, 18.5, 8320.0)

# Aglomerado Nova Maracana Original
a1 = Aglomerado(1, 978.0, 0.22, 0.0, 213.0, 49.0, 'Nova Maracana', m1)

# Aglomerado Nova Maracana Alternativo (5G)
a2 = copy.deepcopy(a1)
a2.id = 2
a2.tipo_cenario = 'Alternativo'
a2.cenario_original = a1
a2.estrategia_atualizacao_bs = 'Acelerada'

# Aglomerado Ubim Original
a3 = Aglomerado(3, 217.0, 0.42, 0.0, 47.0, 21.0, 'Ubim', m1)

# Aglomerado Ubim Alternativo (5G)
a4 = copy.deepcopy(a3)
a4.id = 4
a4.tipo_cenario = 'Alternativo'
a4.cenario_original = a3
a4.estrategia_atualizacao_bs = 'Acelerada'

# Aglomerado Sede Original
a5 = Aglomerado(5, 5118.0, 1.81, 2.0, 1063.0, 174.0, 'Sede', m1)

# Aglomerado Sede Alternativo Greenfield
a6 = copy.deepcopy(a5)
a6.id = 6
a6.tipo_cenario = 'Alternativo'
a6.cenario_original = a5

# Aglomerado Sede Alternativo Greenfield 5G
a7 = copy.deepcopy(a5)
a7.id = 7
a7.tipo_cenario = 'Alternativo'
a7.cenario_original = a5
a7.estrategia_atualizacao_bs = 'Acelerada'

# Aglomerado Sede Alternativo Brownfield 5G
a8 = copy.deepcopy(a5)
a8.id = 8
a8.tipo_cenario = 'Alternativo'
a8.cenario_original = a5
a8.estrategia_atualizacao_bs = 'Acelerada'

# Adicionando infraestrutura existente ao Aglomerado Sede
# 1 BS do Tipo 2G
p1 = Ponto(10.0, 10.0)
b1 = BS(1, TipoBS.MACRO_2G, p1, 0, False, True)

# 1 BS do Tipo 2G
p2 = Ponto(20.0, 20.0)
b2 = BS(2, TipoBS.MACRO_2G, p2, 0, False, True)

# 1 BS do Tipo 3G (BS Hub - central)
p3 = Ponto(30.0, 30.0)
b3 = BS(3, TipoBS.MACRO_3G, p3, 0, True, True)

a5.adicionar_BS(b1)
a5.adicionar_BS(b2)
a5.adicionar_BS(b3)

a8.adicionar_BS(copy.deepcopy(b1))
a8.adicionar_BS(copy.deepcopy(b2))
a8.adicionar_BS(copy.deepcopy(b3))

m1.adicionar_aglomerado(a1)
m1.adicionar_aglomerado(a2)
m1.adicionar_aglomerado(a3)
m1.adicionar_aglomerado(a4)
m1.adicionar_aglomerado(a5)
m1.adicionar_aglomerado(a6)
m1.adicionar_aglomerado(a7)
m1.adicionar_aglomerado(a8)

m1.calcula_demanda_trafego()
m1.calcula_dimensionamento_rede_acesso()
m1.calcula_dimensionamento_rede_transporte()
m1.calcula_dimensionamento_centraloffice()

engine = Engine(m1)
engine.run()
engine.get_graficos()
