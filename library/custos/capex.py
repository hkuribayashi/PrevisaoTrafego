from enum import Enum


class CAPEX(Enum):
    # Reajuste anual de Preços
    TAXA_REAJUSTE = ('Taxa de reajuste de despesas', '%/ano', -0.07)
    TAXA_DEPRECIACAO = ('Taxa de Depreciação Financeira de Eqipamentos', '%/ano', -0.05)

    # Depesas relacionadas à aquisição dos equipamentos (hardware)
    MACRO = ('Macro Base Station', '$/unidade', 1000.0)
    MICRO = ('Micro Base Station', '$/unidade', 1000.0)
    PICO = ('Pico Base Station', '$/unidade', 250.0)
    FEMTO = ('Femto Base Station', '$/unidade', 250.0)

    # Despesas relacioadas à atualização de eequipamentos (hardware)
    ATUALIZACAO_MACRO = ('Macro Base Station', '$/unidade', 100.0)
    ATUALIZACAO_MICRO = ('Micro Base Station', '$/unidade', 100.0)
    ATUALIZACAO_PICO = ('Pico Base Station', '$/unidade', 25.0)
    ATUALIZACAO_FEMTO = ('Femto Base Station', '$/unidade', 25.0)

    # Tempo de Atualização de HW por tipo de BS
    TEMPO_ATUALIZACAO_MACRO = ('Tempo de Atualização de Macro BS', 'horas', 10.0)
    TEMPO_ATUALIZACAO_MICRO = ('Tempo de Atualização de Micro BS', 'horas', 10.0)
    TEMPO_ATUALIZACAO_PICO = ('Tempo de Atualização de Pico BS', 'horas', 1.0)
    TEMPO_ATUALIZACAO_FEMTO = ('Tempo de Atualização de Femto BS', 'horas', 1.0)

    # Tempo de Instalação de HW por tipo de BS
    TEMPO_INSTALACAO_MACRO = ('Tempo de Instalacao de Macro BS', 'horas', 10.0)
    TEMPO_INSTALACAO_MICRO = ('Tempo de Tempo de Instalacao de Micro BS', 'horas', 10.0)
    TEMPO_INSTALACAO_PICO = ('Tempo de Tempo de Instalacao de Pico BS', 'horas', 1.0)
    TEMPO_INSTALACAO_FEMTO = ('Tempo de Instalacao de Femto BS', 'horas', 1.0)

    # Despesas relacionada a RH
    SALARIO_TECNICO = ('Salário do Técnico de Implantação/Atualização', '$/hora', 12.0)
    QTD_TECNICOS_INSTALACAO = ('Qtd de Técnicos por Time de Instalação', 'técnicos/time', 2.0)
    QTD_TECNICOS_ATUALIZACAO = ('Qtd de Técnicos por Time de Atualização', 'técnicos/time', 1.0)
    QTD_TIMES = ('Quantidade de times', 'unidades', 1.0)
    TAXA_CORRECAO_SALARARIO = ('Taxa de Correção de Salário do Técnico de Instalação/Manutenção', '%/ano', 0.07)

    # Despesas de Infraestrutura por BS
    INFRAESTRUTURA_MACRO = ('Despesas de implantação de Infra Macro BS', '$/BS', 1000.0)
    INFRAESTRUTURA_MICRO = ('Despesas de implantação de Infra Micro BS', '$/BS', 1000.0)
    INFRAESTRUTURA_PICO = ('Despesas de implantação de Infra Pico BS', '$/BS', 1000.0)
    INFRAESTRUTURA_FEMTO = ('Despesas de implantação de Infra Femto BS', '$/BS', 1000.0)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "CAPEX descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)
