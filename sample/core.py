import copy

from library.core.engine import Engine
from library.entities.aglomerado import Aglomerado
from library.entities.municipio import Municipio
from library.entities.ponto import Ponto
from library.hetnet.bs import BS
from library.hetnet.tipo_bs import TipoBS


lista_municipios = dict()

######################

# Brownfield + Implantação 5G Lenta: BF+5GS

######################

# Criando um município a partir dos dados de Faro
m1 = Municipio(1, 'Faro', 3272.0, 0.243, 164.0, 0.56, 489.0, 234.0, 134.0, 10, 18.5, 8320.0)
m2 = copy.deepcopy(m1)
m3 = copy.deepcopy(m1)
m4 = copy.deepcopy(m1)

# Nova Maracana
a1 = Aglomerado(1, 978.0, 0.22, 0.0, 213.0, 49.0, 'Nova Maracana', m1)

# Ubim
a2 = Aglomerado(2, 217.0, 0.42, 0.0, 47.0, 21.0, 'Ubim', m1)

# Sede
a3 = Aglomerado(3, 5118.0, 1.81, 2.0, 1063.0, 174.0, 'Sede', m1)

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

a3.adicionar_BS(b1)
a3.adicionar_BS(b2)
a3.adicionar_BS(b3)

m1.adicionar_aglomerado(a1)
m1.adicionar_aglomerado(a2)
m1.adicionar_aglomerado(a3)

lista_municipios['BF+5GS'] = m1

##################################

# Greenfield + Implantação 5G Lenta: GF+5GS

##################################

# Nova Maracana
a4 = Aglomerado(4, 978.0, 0.22, 0.0, 213.0, 49.0, 'Nova Maracana', m2)
a4.tipo_cenario = 'Alternativo'
a4.cenario_original = a1

# Ubim
a5 = Aglomerado(5, 217.0, 0.42, 0.0, 47.0, 21.0, 'Ubim', m2)
a5.tipo_cenario = 'Alternativo'
a5.cenario_original = a2

# Sede
a6 = Aglomerado(6, 5118.0, 1.81, 2.0, 1063.0, 174.0, 'Sede', m2)
a6.tipo_cenario = 'Alternativo'
a6.cenario_original = a3

m2.adicionar_aglomerado(a4)
m2.adicionar_aglomerado(a5)
m2.adicionar_aglomerado(a6)

lista_municipios['GF+5GS'] = m2

##################################

# Brownfield + Implantação 5G Rápida: BF+5GF

##################################

# Nova Maracana
a7 = Aglomerado(7, 978.0, 0.22, 0.0, 213.0, 49.0, 'Nova Maracana', m3)
a7.tipo_cenario = 'Alternativo'
a7.cenario_original = a1
a7.estrategia_atualizacao_bs = 'Acelerada'

# Ubim
a8 = Aglomerado(8, 217.0, 0.42, 0.0, 47.0, 21.0, 'Ubim', m3)
a8.tipo_cenario = 'Alternativo'
a8.cenario_original = a2
a8.estrategia_atualizacao_bs = 'Acelerada'

# Sede
a9 = Aglomerado(9, 5118.0, 1.81, 2.0, 1063.0, 174.0, 'Sede', m3)
a9.tipo_cenario = 'Alternativo'
a9.cenario_original = a3
a9.estrategia_atualizacao_bs = 'Acelerada'

a9.adicionar_BS(copy.deepcopy(b1))
a9.adicionar_BS(copy.deepcopy(b2))
a9.adicionar_BS(copy.deepcopy(b3))

m3.adicionar_aglomerado(a7)
m3.adicionar_aglomerado(a8)
m3.adicionar_aglomerado(a9)

lista_municipios['BF+5GF'] = m3

##################################

# Grenfield + Implantação 5G Rápida: GF+5GF

##################################

# Nova Maracana
a10 = Aglomerado(10, 978.0, 0.22, 0.0, 213.0, 49.0, 'Nova Maracana', m4)
a10.tipo_cenario = 'Alternativo'
a10.cenario_original = a1
a10.estrategia_atualizacao_bs = 'Acelerada'

# Ubim
a11 = Aglomerado(11, 217.0, 0.42, 0.0, 47.0, 21.0, 'Ubim', m4)
a11.tipo_cenario = 'Alternativo'
a11.cenario_original = a2
a11.estrategia_atualizacao_bs = 'Acelerada'

# Sede
a12 = Aglomerado(12, 5118.0, 1.81, 2.0, 1063.0, 174.0, 'Sede', m4)
a12.tipo_cenario = 'Alternativo'
a12.cenario_original = a3
a12.estrategia_atualizacao_bs = 'Acelerada'

m4.adicionar_aglomerado(a10)
m4.adicionar_aglomerado(a11)
m4.adicionar_aglomerado(a12)

lista_municipios['GF+5GF'] = m4

engine = Engine(lista_municipios)
engine.run()
engine.get_graficos()
