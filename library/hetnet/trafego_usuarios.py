from enum import Enum


class TrafegoUsuariosMoveis(Enum):

    CONFIG_DEFAULT = (0.8, 5.0, 0.55, 0.95, 0.55, 0.16)

    def __init__(self, proporcao_final_terminais_heavy, inicio_adocao, taxa_crescimento_terminais_heavy, proporcao_final_usuario_internet,
                 taxa_crescimento_usuarios_internet, taxa_usuarios_ativos):
        self.proporcao_final_terminais_heavy = proporcao_final_terminais_heavy  # mi/determina a taxa final de adoção de terminais do tipo heavy
        self.inicio_adocao = inicio_adocao                                    # Beta da Curva de Gompertz
        self.taxa_crescimento_terminais_heavy = taxa_crescimento_terminais_heavy  # gamma/taxa de adoção dos terminais do tipo j
        self.proporcao_final_usuario_internet = proporcao_final_usuario_internet  # mu/determina a taxa final de adoção de internet por usuário
        self.taxa_crescimento_usuarios_internet = taxa_crescimento_usuarios_internet  # gamma/taxa de adocao de internet
        self.taxa_usuarios_ativos = taxa_usuarios_ativos
