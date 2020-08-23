import numpy as np
import matplotlib.pyplot as plt

from library.util.util import get_gompertz

# Teste para geracao de taxa de usuários de Internet
tx = 10
time = np.arange(tx)

c = 0.15
h = get_gompertz(0.95, 5, c, tx)

c = 0.25
h1 = get_gompertz(0.95, 10, c, tx)

h2 = get_gompertz(0.65, 30, 1.15, tx)

# plt.plot(h, 'g-*', label='c=0.15')
# plt.plot(h1, 'b--', label='c=0.25')
# plt.plot(h2, 'r-.', label='c=0.35')

plt.xlabel('Período de Análise (Anos)')
plt.ylabel('Taxa de Usuários de Internet')
plt.legend(loc='upper left')
plt.grid(linestyle=':')

plt.savefig('{}Temp.eps'.format('/Users/hugo/Desktop/'), dpi=600, bbox_inches='tight')
plt.close()
