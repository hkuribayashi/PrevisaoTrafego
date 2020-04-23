from library.entities import Aglomerado
from library.hetnet import Operadora
from library.hetnet import BS
from library.hetnet import BSType

# area [km2]
# densidade_populacional [habitantes/km2]
# tempo_analise [anos]
# populacao_ativa [Taxa]
# proporcao_final_terminais_heavy [Taxa]
# taxa_crescimento_terminais_heavy [Taxa]
# proporcao_final_usuario_internet [Taxa]
# taxa_crescimento_usuarios_internet [Taxa]
# Taxa de usuários móveis ativos [Taxa]


a1 = Aglomerado(1.81, 2828.0, 15, 0.56, 0.8, 0.45, 0.95, 0.45, 0.16)
b1 = BS(1, Operadora.operadora1, BSType.MACRO_2G)
b2 = BS(2, Operadora.operadora1, BSType.MACRO_3G)

a1.lista_bs.append(b1)
a1.lista_bs.append(b2)

a1.calcula_demanda_trafego()
a1.calcula_capacidade_rede_acesso()
a1.debug()