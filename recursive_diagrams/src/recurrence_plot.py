from math import ceil
from typing import Callable, Literal

def recurrence_field_values(
  f: list[float],
  D: int,
  d: int = 1,
  ord: Literal[1, 2, 'inf'] = 2
) -> tuple[int, list[float]]:
  
  assert len(f) > 0
  
  N: int = len(f) - 1
  M: int = N - (D - 1) * d
  field_values: list[float] = [ 0 ] * ( (M + 1) * (M + 1) )
  
  norm_fn_lookup: dict[Literal[1, 2, 'inf'], Callable] = {
    1: lambda xs: sum([ abs(x) for x in xs]),
    2: lambda xs: sum([ x**2 for x in xs]) ** 0.5,
    'inf': lambda xs: max([ abs(x) for x in xs])
  }
  
  norm_fn: Callable = norm_fn_lookup[ord]
  
  for i in range(M + 1):
    for j in range(M + 1):
      y_i = [ f[i + k * d] for k in range(D) ]
      y_j = [ f[j + k * d] for k in range(D) ]
      diff = [ a - b for a, b in zip(y_i, y_j) ]
      field_values[j + i * (M + 1)] = norm_fn(diff)
  
  return (M + 1, field_values)

def recurrence_plot_custom(
  f: list[float], 
  D: int, 
  p: float,
  d: int = 1,
  ord: Literal[1, 2, 'inf'] = 2
) -> tuple[int, list[bool]]:
  """
  Custom recurrence plot implementation with the ability to specify what percentage of pixels should be colored black.
  
  :param f: Signal values
  :type f: list[float]
  :param D: Number of samples per vector
  :type D: int
  :param p: Percentage of pixels which should be colored black.
  :type p: float
  :param d: Stride
  :type d: int
  :param ord: type of L norm
  :type ord: Literal[1, 2, 'inf']
  """
  size, field_values = recurrence_field_values(f, D, d, ord)
  r = choose_r(field_values, p)
  # print('chosen r = ', r)
  return (size, [ v > r for v in field_values ])

def choose_r(values: list[float], p: float) -> float:
  """
  Choose r such that the percentage of values smaller or equal to r would be as close to p as possible.
  
  :param values: Values to fit r to
  :type values: list[float]
  :param p: Target percentage
  :type p: float
  """
  k = ceil((1 - p) * len(values))
  return sorted(values)[k - 1]

def recurrence_plot(
  f: list[float], 
  D: int, 
  r: float, 
  d: int = 1, 
  ord: Literal[1, 2, 'inf'] = 2
) -> tuple[int, list[bool]]:
  """
  Default implementation of the recurrence plot.
  
  :param f: Signal values
  :type f: list[float]
  :param D: Number of samples per vector
  :type D: int
  :param r: Threshold value
  :type r: float
  :param d: Stride
  :type d: int
  :param ord: type of L norm
  :type ord: Literal[1, 2, 'inf']
  """
  size, field_values = recurrence_field_values(f, D, d, ord)
  return (size, [ v > r for v in field_values ])