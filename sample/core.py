from library.entities.Aglomerado import Aglomerado
from library.entities.Municipio import Municipio
from library.hetnet.BS import BS
from library.hetnet.BSType import BSType

# Criando um município a partir dos dados de Faro
# total_alunos, percentual_ead, total_docentes, percentual_pop_ativa, total_servidores_publicos,
# total_servidores_publicos_saude, total_veiculos, tempo_analise
m1 = Municipio(1, 3272.0, 0.243, 164.0, 0.56, 489.0, 234.0, 134.0, 15)

# total_habitantes, area_aglomerado, total_agencias_bancarias, total_domicilios
a1 = Aglomerado(1, 2828.0, 1.81, 2.0, 1063.0, m1.percentual_pop_ativa)  # Aglomerado Sede

# Adicionando infraestrutura existente ao Aglomerado
b1 = BS(1, BSType.MACRO_2G)  # 1 BS do Tipo 2G
b2 = BS(2, BSType.MACRO_3G)  # 1 BS do Tipo 3G

a1.adicionar_BS(b1)
a1.adicionar_BS(b2)

m1.adicionar_aglomerado(a1)

m1.calcula_demanda_trafego()
m1.calcula_dimensionamento_rede_acesso()
