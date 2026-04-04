# %%

import cmath
import numpy as np
import matplotlib.pyplot as plt
from src.fft import cooley_tukey_fft

N = 2 ** 10

omega = 10 * 2 * cmath.pi
ts = np.linspace(0, 0.5, N, endpoint=False)
xs = np.zeros_like(ts)
for n in range(1, 6):
  xs += n * np.cos(n * omega * ts)

plt.plot(ts, xs)

# %%

dt = ts[1] - ts[0]
freqs = np.zeros(N)
for k in range(N):
  if k < N // 2:
    freqs[k] = k / (N * dt)
  else:
    freqs[k] = (k - N) / (N * dt)

XS = cooley_tukey_fft(xs)

mask = (freqs >= 0) & (freqs < 100)

amplitude = np.abs(XS) / N
amplitude[1:N//2] *= 2

plt.plot(freqs[mask], amplitude[mask])