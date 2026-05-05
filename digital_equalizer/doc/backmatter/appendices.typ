#heading(numbering: none, "Priedai")

Dokumentą sudaro vienas priedas -- @fft-impl[Kodo fragmentas]

#figure([
```py
def cooley_tukey_ifft(xs):
  n = len(xs)

  if n == 0:
    return []

  def _cooley_tukey_ifft(values):
    m = len(values)

    if m == 1:
      return [complex(values[0])]
    if m % 2 != 0:
      raise ValueError("Input length must be a power of 2")

    even = _cooley_tukey_ifft(values[0::2])
    odd = _cooley_tukey_ifft(values[1::2])

    signal = [0j] * m
    half = m // 2

    for k in range(half):
      twiddle = cmath.exp(2j * cmath.pi * k / m)
      t = twiddle * odd[k]
      signal[k] = even[k] + t
      signal[k + half] = even[k] - t

    return signal

  signal = _cooley_tukey_ifft(xs)
  return [value / n for value in signal]
```
  ],
  caption: [Cooley-Tukey FFT algoritmo įgyvendinimas]
) <fft-impl>