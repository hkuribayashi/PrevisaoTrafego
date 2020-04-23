from enum import Enum


class AplicacaoFaroSede(Enum):

    E_HEALTH_1 = (1, 'Monitoramento de Saúde', 1.0, 0.3, 5.0, 0.35, 1.0, 5118.0)
    E_HEALTH_2 = (2, 'Telemedicina', 25.0, 1.0, 5.0, 0.35, 0.4, 5.0)
    E_HEALTH_3 = (3, 'Navegação Web', 2.0, 1.0, 5.0, 0.55, 0.5, 190.0)

    E_LEARNING_4 = (4, 'EaD', 13.9, 1.0, 5.0, 0.55, 0.16, 645.0)
    E_LEARNING_5 = (5, 'Navegação Web', 2.0, 1.0, 5.0, 0.55, 0.16, 2786)

    E_GOV_6 = (6, 'Monitoramento de Vias', 8.0, 1.0, 10.0, 0.55, 1.0, 174.0)
    E_GOV_7 = (7, 'Navegação Web', 2.0, 1.0, 5.0, 0.55, 0.16, 396.0)

    E_FINANCE_8 = (8, 'Caixas Eletrônicos', 2.0, 1.0, 5.0, 0.55, 0.16, 10.0)
    E_FINANCE_9 = (9, 'Aplicações Financeiras', '2.0', 1.0, 5.0, 0.55, 0.16, 2470.0)

    IOT_10 = (10, 'Smart water measurement', 0.1, 10.0, 15, 0.55, 1.0, 1063.0)
    IOT_11 = (11, 'Smart electricity measurement', 0.1, 1.0, 15.0, 0.55, 1.0, 1063.0)
    IOT_12 = (12, 'GPS Tracking', 0.1, 1.0, 5.0, 0.45, 1.0, 109.0)

    def __init__(self, id_, aplicacao, vazao, mu, beta, gamma, alpha, qtd_terminais):
        self._id = id_
        self._aplicacao = aplicacao
        self._vazao = vazao
        self._mu = mu
        self._beta = beta
        self._gamma = gamma
        self._alpha = alpha
        self._qtd_terminais = qtd_terminais

    @property
    def id(self):
        return self._id

    @property
    def aplicacao(self):
        return self._aplicacao

    @property
    def vazao(self):
        return self._vazao

    @property
    def mu(self):
        return self._mu

    @property
    def beta(self):
        return self._beta

    @property
    def gamma(self):
        return self._gamma

    @property
    def alpha(self):
        return self._alpha

    @property
    def qtd_terminais(self):
        return self._qtd_terminais
