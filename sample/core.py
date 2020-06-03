from library.entities.Aglomerado import Aglomerado
from library.entities.Municipio import Municipio
from library.entities.Ponto import Ponto
from library.hetnet.BS import BS
from library.hetnet.TipoBS import TipoBS
from library.tco.CAPEX import CAPEX

# Criando um município a partir dos dados de Faro
# total_alunos, percentual_ead, total_docentes, percentual_pop_ativa, total_servidores_publicos,
# total_servidores_publicos_saude, total_veiculos, tempo_analise
m1 = Municipio(1, 3272.0, 0.243, 164.0, 0.56, 489.0, 234.0, 134.0, 15)

# id, total_habitantes, area_aglomerado, total_agencias_bancarias, total_domicilios, percentagem_pop_ativa, total_cruzamentos
a1 = Aglomerado(1, 978.0, 0.22, 0.0, 213.0, m1.percentual_pop_ativa, 49.0, 'Nova Maracana')  # Aglomerado Nova Maracana
a2 = Aglomerado(2, 217.0, 0.42, 0.0, 47.0, m1.percentual_pop_ativa, 21.0, 'Ubim')  # Aglomerado Ubim
a3 = Aglomerado(3, 5118.0, 1.81, 2.0, 1063.0, m1.percentual_pop_ativa, 174.0, 'Sede')  # Aglomerado Sede

# Adicionando infraestrutura existente ao Aglomerado
p1 = Ponto(10.0, 10.0)
b1 = BS(1, TipoBS.MACRO_2G, p1, 0, False, True)  # 1 BS do Tipo 2G

p2 = Ponto(20.0, 20.0)
b2 = BS(2, TipoBS.MACRO_2G, p2, 0, False, True)  # 1 BS do Tipo 2G

p3 = Ponto(30.0, 30.0)
b3 = BS(3, TipoBS.MACRO_3G, p3, 0, True, True)  # 1 BS do Tipo 3G (BS Hub - central)



a3.adicionar_BS(b1)
a3.adicionar_BS(b2)
a3.adicionar_BS(b3)

m1.adicionar_aglomerado(a1)
m1.adicionar_aglomerado(a2)
m1.adicionar_aglomerado(a3)

m1.calcula_demanda_trafego()
m1.calcula_dimensionamento_rede_acesso()
m1.calcula_dimensionamento_rede_transporte()
m1.calcula_dimensionamento_centraloffice()

c = CAPEX(m1)
c.calcula_capex()