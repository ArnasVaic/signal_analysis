import cmath


def cooley_tukey_fft(xs):
  """Compute the FFT of a sequence using recursive radix-2 Cooley-Tukey.

  This implementation is intentionally simple and readable.
  Input length must be a power of 2.
  """
  n = len(xs)

  if n == 0:
    return []
  if n == 1:
    return [complex(xs[0])]
  if n % 2 != 0:
    raise ValueError("Input length must be a power of 2")

  even = cooley_tukey_fft(xs[0::2])
  odd = cooley_tukey_fft(xs[1::2])

  spectrum = [0j] * n
  half = n // 2

  for k in range(half):
    twiddle = cmath.exp(-2j * cmath.pi * k / n)
    t = twiddle * odd[k]
    spectrum[k] = even[k] + t
    spectrum[k + half] = even[k] - t

  return spectrum
