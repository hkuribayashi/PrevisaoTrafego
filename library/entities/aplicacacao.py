from enum import Enum

# 2806
class Aplicacao(Enum):

    E_HEALTH_1 = (1, 'Monitoramento de Saúde', 1.0, 0.3, 15.0, 0.55, 1.0)
    E_HEALTH_2 = (2, 'Telemedicina', 25.0, 1.0, 15.0, 0.55, 0.4)
    E_HEALTH_3 = (3, 'Navegação Web', 2.0, 1.0, 15.0, 0.55, 0.5)

    E_LEARNING_4 = (4, 'EaD', 13.9, 1.0, 15.0, 0.55, 0.16)
    E_LEARNING_5 = (5, 'Navegação Web', 2.0, 1.0, 15.0, 0.55, 0.16)

    E_GOV_6 = (6, 'Monitoramento de Vias', 8.0, 1.0, 15.0, 0.55, 1.0)
    E_GOV_7 = (7, 'Navegação Web', 2.0, 1.0, 15.0, 0.55, 0.16)

    E_FINANCE_8 = (8, 'Caixas Eletrônicos', 2.0, 1.0, 10.0, 0.55, 0.16)
    E_FINANCE_9 = (9, 'Aplicações Financeiras', 2.0, 1.0, 10.0, 0.55, 0.16)

    IOT_10 = (10, 'Smart water measurement', 0.1, 1.0, 15.0, 0.55, 1.0)
    IOT_11 = (11, 'Smart electricity measurement', 0.1, 1.0, 15.0, 0.55, 1.0)
    IOT_12 = (12, 'GPS Tracking', 0.1, 1.0, 15.0, 0.45, 1.0)

    def __init__(self, id_, nome, vazao, mu, beta, gamma, alpha):
        self.id = id_
        self.nome = nome
        self.vazao = vazao
        self.mu = mu
        self.beta = beta
        self.gamma = gamma
        self.alpha = alpha
