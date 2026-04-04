import cmath

def dft(xs):
  N = len(xs)
  XS = [ 0j ] * N
  for k in range(N):
    s = 0j
    for n in range(N):
      s += xs[n] * cmath.exp(-2j * cmath.pi * k * n / N)
    XS[k] = s
  return XS