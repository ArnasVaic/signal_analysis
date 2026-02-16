# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from recurrence_plot import recurrence_plot_custom, recurrence_plot
from render_plot import render_recurrence_plot
import calendar

df = pd.read_excel('../data/litgrid/litgrid-2025.xls')

signal = df['fact'].squeeze().tolist()

# Generate recurrence diagrams + combine into single image

year = 2025
days_in_month = [
  calendar.monthrange(year, month)[1] for month in range(1, 13)
]

DAYS_PER_RP = min(days_in_month)

# # datapoints have 15 min intervals
PTS_PER_DAY = 24 * 4 

result = None
plots = []

for month in tqdm(range(12)):
  
  days = sum(days_in_month[:month])
  
  print(days)
  
  offset = days * PTS_PER_DAY
  
  start = offset
  end = offset + DAYS_PER_RP * PTS_PER_DAY
  f = signal[start : end]

  s, plot = recurrence_plot_custom(f, D=2, p=0.3, d=1, ord='inf')
  
  plots.append(plot)
  
  # on offset initialize result with correct size (depends on params)
  if result is None:
    result = np.zeros((s, s))
  else:
    assert len(plot) == result.size
  
  plot = np.reshape(plot, shape=(s, s))

  result = result + plot
