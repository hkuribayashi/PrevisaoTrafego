import numpy as np
import matplotlib.pyplot as plt

from library.util.Util import get_gompertz

# Teste para geracao de taxa de usuários de Internet
a = 0.95
tx = 10
time = np.arange(tx)

b = 5
c = 0.15
h = get_gompertz(a, b, c, tx)

b = 5
c = 0.25
h1 = get_gompertz(a, b, c, tx)

b = 5
c = 0.35
h2 = get_gompertz(a, b, c, tx)

b = 5
c = 0.45
h3 = get_gompertz(a, b, c, tx)


plt.plot(h, 'g-*', label='b=5')
plt.plot(h1, 'b--', label='b=10')
plt.plot(h2, 'r-.', label='b=15')
plt.plot(h3, '-o', label='b=25')
plt.xlabel('Período de Análise (Anos)')
plt.ylabel('Taxa de Usuários de Internet')
plt.legend(loc='upper left')
plt.grid(linestyle=':')
plt.show()
