from library.entities import Aglomerado
from library.hetnet import Operadora
from library.hetnet import BS
from library.hetnet import BSType

# area, densidade_populacional, tempo_analise, populacao_ativa, numero_terminais_educacao,
# numero_terminais_saude, numero_terminais_comercio, numero_terminais_governanca,
# numero_terminais_seguranca, proporcao_final_terminais_heavy, taxa_crescimento_terminais_heavy,
# proporcao_final_usuario_internet, taxa_crescimento_usuarios_internet


a1 = Aglomerado(100.0, 100.0, 15, 0.9, 60, 40, 20, 10, 10, 0.8, 0.45, 0.95, 0.45, 0.16)
b1 = BS(1, Operadora.operadora1, BSType.MACRO_2G, a1)
b2 = BS(2, Operadora.operadora1, BSType.MACRO_3G, a1)

a1.lista_bs.append(b1)
a1.lista_bs.append(b2)

a1.calcula_demanda_trafego()
a1.calcula_capacidade_rede_acesso()