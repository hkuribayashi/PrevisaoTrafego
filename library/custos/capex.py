from enum import Enum


class CAPEX(Enum):
    # Reajuste anual de Preços
    TAXA_REAJUSTE = ('Taxa de reajuste de despesas', '%/ano', -0.03)

    # Rádio
    # Despesas de Infraestrutura por BS
    INFRAESTRUTURA_MACRO = ('Despesas de implantação de Infra Macro BS', '$/BS', 1.0)
    INFRAESTRUTURA_MICRO = ('Despesas de implantação de Infra Micro BS', '$/BS', 0.5)
    INFRAESTRUTURA_FEMTO = ('Despesas de implantação de Infra Femto BS', '$/BS', 0.05)

    # Despesas relacioadas à atualização de eequipamentos (hardware)
    ATUALIZACAO_MACRO = ('Macro Base Station', '$/unidade', 0.2727)
    ATUALIZACAO_MICRO = ('Micro Base Station', '$/unidade', 0.13)
    ATUALIZACAO_FEMTO = ('Femto Base Station', '$/unidade', 0.0)

    # Depesas relacionadas à aquisição dos equipamentos (hardware)
    MACRO_3G = ('Macro Base Station 3G', '$/unidade', 0.3454)
    MACRO_4G = ('Macro Base Station 4G', '$/unidade', 0.3718)
    MACRO_45G = ('Macro Base Station 4.5G', '$/unidade', 0.3718)
    MACRO_5G = ('Macro Base Station 5G', '$/unidade', 0.4636)

    MICRO_3G = ('Micro Base Station 3G', '$/unidade', 0.1727)
    MICRO_4G = ('Micro Base Station 4G', '$/unidade', 0.1859)
    MICRO_45G = ('Micro Base Station 4.5G', '$/unidade', 0.1859)
    MICRO_5G = ('Micro Base Station 5G', '$/unidade', 0.2181)

    FEMTO_4G = ('Femto Base Station 4G', '$/unidade', 0.0557)
    FEMTO_45G = ('Femto Base Station 4.5G', '$/unidade', 0.0557)
    FEMTO_5G = ('Femto Base Station 5G', '$/unidade', 0.0654)

    # Tempo de Atualização de HW por tipo de BS
    TEMPO_ATUALIZACAO_MACRO = ('Tempo de Atualização de Macro BS', 'horas', 10.0)
    TEMPO_ATUALIZACAO_MICRO = ('Tempo de Atualização de Micro BS', 'horas', 10.0)
    TEMPO_ATUALIZACAO_FEMTO = ('Tempo de Atualização de Femto BS', 'horas', 1.0)

    # Tempo de Instalação de HW por tipo de BS
    TEMPO_INSTALACAO_MACRO = ('Tempo de Instalacao de Macro BS', 'horas', 10.0)
    TEMPO_INSTALACAO_MICRO = ('Tempo de Tempo de Instalacao de Micro BS', 'horas', 10.0)
    TEMPO_INSTALACAO_FEMTO = ('Tempo de Instalacao de Femto BS', 'horas', 1.0)

    # Despesas relacionada a RH
    SALARIO_TECNICO = ('Salário do Técnico de Implantação/Atualização', '$/hora', 0.0004727)
    QTD_TECNICOS_INSTALACAO = ('Qtd de Técnicos por Time de Instalação', 'técnicos/time', 2.0)
    QTD_TECNICOS_ATUALIZACAO = ('Qtd de Técnicos por Time de Atualização', 'técnicos/time', 2.0)
    QTD_TIMES = ('Quantidade de times', 'unidades', 1.0)
    TAXA_CORRECAO_SALARARIO = ('Taxa de Correção de Salário do Técnico de Instalação/Manutenção', '%/ano', 0.07)

    def __init__(self, descricao, unidade_medida, valor):
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.valor = valor

    def __str__(self):
        return "CAPEX descricao={}, unidade_medida={}, valor={}".format(self.descricao, self.unidade_medida, self.valor)
