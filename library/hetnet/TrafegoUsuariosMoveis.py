from enum import Enum


class TrafegoUsuariosMoveis(Enum):

    CONFIG_DEFAULT = (0.8, 5.0, 0.55, 0.95, 0.55, 0.16)

    def __init__(self, proporcao_final_terminais_heavy, inicio_adocao, taxa_crescimento_terminais_heavy, proporcao_final_usuario_internet,
                 taxa_crescimento_usuarios_internet, taxa_usuarios_ativos):
        self._proporcao_final_terminais_heavy = proporcao_final_terminais_heavy  # mi/determina a taxa final de adoção de terminais do tipo heavy
        self._inicio_adocao = inicio_adocao                                    # Beta da Curva de Gompertz
        self._taxa_crescimento_terminais_heavy = taxa_crescimento_terminais_heavy  # gamma/taxa de adoção dos terminais do tipo j
        self._proporcao_final_usuario_internet = proporcao_final_usuario_internet  # mu/determina a taxa final de adoção de internet por usuário
        self._taxa_crescimento_usuarios_internet = taxa_crescimento_usuarios_internet  # gamma/taxa de adocao de internet
        self._taxa_usuarios_ativos = taxa_usuarios_ativos

    @property
    def proporcao_final_terminais_heavy(self):
        return self._proporcao_final_terminais_heavy

    @property
    def inicio_adocao(self):
        return self._inicio_adocao

    @property
    def taxa_crescimento_terminais_heavy(self):
        return self._taxa_crescimento_terminais_heavy

    @property
    def proporcao_final_usuario_internet(self):
        return self._proporcao_final_usuario_internet

    @property
    def taxa_crescimento_usuarios_internet(self):
        return self._taxa_crescimento_usuarios_internet

    @property
    def taxa_usuarios_ativos(self):
        return self._taxa_usuarios_ativos
