from aglomerado import Aglomerado


# area, densidade_populacional, tempo_analise, populacao_ativa, numero_terminais_educacao,
# numero_terminais_saude, numero_terminais_comercio, numero_terminais_governanca,
# numero_terminais_seguranca, proporcao_final_terminais_heavy, taxa_crescimento_terminais_heavy,
# proporcao_final_usuario_internet, taxa_crescimento_usuarios_internet

a1 = Aglomerado(100.0, 100.0, 15, 0.9, 60, 40, 20, 10, 10, 0.65, 0.3, 0.9, 0.3)
a1.calcula_demanda_trafego()
a1.debug()
