from library.tco.CAPEX import CAPEX
from library.tco.OPEX import OPEX


class TCO:

    def __init__(self, municipio):
        self.capex = CAPEX(municipio)
        self.opex = OPEX(municipio)

    def calcula_capex(self):
        self.capex.calcula_capex()

    def calcula_opex(self):
        self.opex.calcula_opex(self.capex)
