import numpy as np
import matplotlib.pyplot as plt

from util import get_gompertz

# Teste para geracao de taxa de usuários de Internet
a = 0.95
c = 0.45
tx = 15
time = np.arange(tx)

b = 5
h = get_gompertz(a, b, c, tx)

b = 10
h1 = get_gompertz(a, b, c, tx)

b = 15
h2 = get_gompertz(a, b, c, tx)

b = 20
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


# Teste para geracao de taxa de terminais heavy
a = 0.8
c = 0.45

b=5
z = get_gompertz(a, b, c, tx)
z_o = 1 - z

b=10
z1 = get_gompertz(a, b, c, tx)
z1_o = 1 - z1

plt.plot(z, 'g-*', label='Heavy Users b=5')
plt.plot(z_o, 'g--', label='Ordinary Users b=5')
plt.plot(z1, 'r-*', label='Heavy Users b=10')
plt.plot(z1_o, 'r--', label='Ordinary Users b=10')
plt.grid(linestyle=':')
plt.ylim([0.0, 1.1])
plt.legend(loc='upper right')
plt.show()