import numpy as np
import matplotlib.pyplot as plt

from library.util.Util import get_gompertz

# Teste para geracao de taxa de usuários de Internet
a = 0.95
b = 5
tx = 10
time = np.arange(tx)


c = 0.15
h = get_gompertz(a, b, c, tx)

c = 0.25
h1 = get_gompertz(a, b, c, tx)

c = 0.35
h2 = get_gompertz(a, b, c, tx)

c = 0.45
h3 = get_gompertz(a, b, c, tx)

plt.plot(h, 'g-*', label='c=0.15')
plt.plot(h1, 'b--', label='c=0.25')
plt.plot(h2, 'r-.', label='c=0.35')
plt.plot(h3, '-o', label='c=0.45')
plt.xlabel('Período de Análise (Anos)')
plt.ylabel('Taxa de Usuários de Internet')
plt.legend(loc='upper left')
plt.grid(linestyle=':')
plt.show()
