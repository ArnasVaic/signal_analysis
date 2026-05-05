# %%

import cmath
import numpy as np
import matplotlib.pyplot as plt
from src.dft import dft

ts = np.linspace(0, 25, 1000)
xs = 2 * np.sin(2 * cmath.pi * ts / 25) + np.cos(8 * cmath.pi * ts / 25)

XS = dft(xs)

# %%
plt.title('x(t)')
plt.scatter(ts, xs)

# %%
plt.title('Re(X(t))')
plt.scatter(ts, np.real(XS))

# %%
plt.title('Im(X(t))')
plt.scatter(ts, np.imag(XS))