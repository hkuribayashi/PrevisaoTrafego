from abc import ABC, abstractmethod


class TCO(ABC):

    def __init__(self, municipio, componente):
        self.municipio = municipio
        self.tipos_rede_radio = ['Macro', 'Hetnet']
        self.componente = componente

    def get_tco(self):
        self.get_capex()
        self.get_opex()

    def get_capex(self):
        for ag in self.municipio.aglomerados:
            print('CAPEX de {} do Aglomerado {}:'.format(self.componente, ag.id))

            for tipo in self.tipos_rede_radio:
                if tipo == 'Macro' and self.componente == 'Radio':
                    param_1 = ag.lista_bs['implantacao_macro']
                    param_2 = None
                    componente_tco = ag.capex_macro[self.componente]
                elif tipo == 'Hetnet' and self.componente == 'Radio':
                    param_1 = ag.lista_bs['implantacao_hetnet']
                    param_2 = None
                    componente_tco = ag.capex_hetnet[self.componente]
                elif tipo == 'Macro' and self.componente == 'Transporte':
                    param_1 = ag.qtd_antena_mw_macro
                    param_2 = ag.qtd_sw_carrier_mw_macro_only
                    componente_tco = ag.capex_macro[self.componente]
                elif tipo == 'Hetnet' and self.componente == 'Transporte':
                    param_1 = ag.qtd_antena_mw_hetnet
                    param_2 = ag.qtd_sw_carrier_mw_hetnet
                    componente_tco = ag.capex_hetnet[self.componente]
                else:
                    raise RuntimeError('[TCO] Tipo de Rede não Encontrada: {} {}'.format(self.componente, tipo))

                equip_atualizacao, instal_atualizacao = self.get_capex_atualizacoes(param_1)
                equip_novos, instal_novos = self.get_capex_implantacoes(param_1, param_2)
                infraestrutura = self.get_capex_infraestrutura(param_1, self.componente)

                componente_tco['infraestrutura'] += infraestrutura
                componente_tco['equipamentos'] += equip_atualizacao
                componente_tco['equipamentos'] += equip_novos
                componente_tco['instalacao'] += instal_atualizacao
                componente_tco['instalacao'] += instal_novos

                print('Implantação de {} {}'.format(self.componente, tipo))
                print('CAPEX Infraestrutura:')
                print(infraestrutura)
                print('CAPEX Equipamentos Novos:'.format(self.componente))
                print(equip_novos)
                print('CAPEX Equipamentos Atualizados:')
                print(equip_atualizacao)
                print('CAPEX Instalação de Equipamentos Novos:')
                print(instal_novos)
                print('CAPEX Instalação de Atualização de Equipamentos:')
                print(instal_atualizacao)
                print()

    def get_opex(self):
        for ag in self.municipio.aglomerados:
            print('OPEX de {} do Aglomerado {}:'.format(self.componente, ag.id))

            for tipo in self.tipos_rede_radio:
                if tipo == 'Macro' and self.componente == 'Radio':
                    param_1 = ag.lista_bs['implantacao_macro']
                    param_2 = None
                    componente_tco = ag.opex_macro[self.componente]
                elif tipo == 'Hetnet' and self.componente == 'Radio':
                    param_1 = ag.lista_bs['implantacao_hetnet']
                    param_2 = None
                    componente_tco = ag.opex_hetnet[self.componente]
                elif tipo == 'Macro' and self.componente == 'Transporte':
                    param_1 = ag.qtd_antena_mw_macro
                    param_2 = ag.qtd_sw_carrier_mw_macro_only
                    componente_tco = ag.opex_macro[self.componente]
                elif tipo == 'Hetnet' and self.componente == 'Transporte':
                    param_1 = ag.qtd_antena_mw_hetnet
                    param_2 = ag.qtd_sw_carrier_mw_hetnet
                    componente_tco = ag.opex_hetnet[self.componente]
                else:
                    raise RuntimeError('[TCO] Tipo de Rede não Encontrada: {} {}'.format(self.componente, tipo))

                componente_tco['energia'] = self.get_opex_energia(param_1, param_2)
                componente_tco['manutencao'] = self.get_opex_manutencao(param_1, param_2)
                componente_tco['aluguel'] = self.get_opex_aluguel(param_1)
                componente_tco['falhas'] = self.get_opex_falhas(param_1, param_2)

                print('Implantação {}'.format(self.componente))
                print('OPEX Energia:')
                print(componente_tco['energia'])
                print('OPEX manutencao:')
                print(componente_tco['manutencao'])
                print('OPEX aluguel:')
                print(componente_tco['aluguel'])
                print('OPEX falhas:')
                print(componente_tco['falhas'])
                print()

    @abstractmethod
    def get_capex_implantacoes(self, param_1, param_2):
        pass

    @abstractmethod
    def get_capex_atualizacoes(self, param_1):
        pass

    @abstractmethod
    def get_capex_infraestrutura(self, param_1, param_2):
        pass

    @abstractmethod
    def get_opex_energia(self, param_1, param_2):
        pass

    @abstractmethod
    def get_opex_manutencao(self, param_1, param_2):
        pass

    @abstractmethod
    def get_opex_aluguel(self, param_1):
        pass

    @abstractmethod
    def get_opex_falhas(self, param_1, param_2):
        pass
