#heading(numbering: none, "Priedai")

Dokumentą sudaro du priedai @classic_rd[Kodo fragmentas] ir @custom_rd[Kodo fragmentas].

#figure([
```py
from math import ceil
from typing import Callable, Literal

def recurrence_plot(
  f: list[float], 
  D: int, 
  r: float, 
  d: int = 1, 
  ord: Literal[1, 2, 'inf'] = 2
) -> tuple[int, list[bool]]:
  size, field_values = recurrence_field_values(f, D, d, ord)
  return (size, [ v > r for v in field_values ])

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
```],
caption: "Klasikinio rekurentinių diagramų algoritmo įgyvendinimas"
) <classic_rd>

@classic_rd[Kodo fragmente] pateiktas klasikinio rekurentinių diagramų algoritmo įgyvendinimas `python` programavimo kalba nenaudojant jokių išorinių pagalbinių paketų išskyrus standartinės bibliotekos pagalbinę funkciją `Ceil` ir tipų aprašymo konstrukcijas `Callable` ir `Literal`. Didelė algoritmo dalis yra iškelta į metodą `recurrence_field_values`, kuris yra naudojamas įgyvendinant ir pritaikytą algoritmą, kuris palaiko parametrą $p$.

#figure(
  caption: "Pritaikyto rekurentinių diagramų algoritmo įgyvendinimas", 
[```py
def recurrence_plot_custom(
  f: list[float], 
  D: int, 
  p: float,
  d: int = 1,
  ord: Literal[1, 2, 'inf'] = 2
) -> tuple[int, list[bool]]:
  size, field_values = recurrence_field_values(f, D, d, ord)
  r = choose_r(field_values, p)
  return (size, [ v > r for v in field_values ])

def choose_r(values: list[float], p: float) -> float:
  k = ceil(p * len(values))
  return sorted(values)[k - 1]
```]
) <custom_rd>

@custom_rd[Kodo fragmente] pateiktas pritaikyto algoritmo įgyvendinimas. Palaikomas parametras $p$, kuris nustato juodų taškų procentą diagramoje. Panaudota praeitame priede @classic_rd pateikta funkcija `recurrence_field_values`.