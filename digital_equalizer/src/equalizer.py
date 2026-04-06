import numpy as np

from src.fft import cooley_tukey_fft, cooley_tukey_ifft

def eq(xs, sr, gain):
  N = len(xs)
  XS = cooley_tukey_fft(xs)
  freqs = np.fft.fftfreq(N, d=1/sr)
  for k in range(N):
    XS[k] *= gain(freqs[k])
  new_xs = cooley_tukey_ifft(XS)
  return new_xs
