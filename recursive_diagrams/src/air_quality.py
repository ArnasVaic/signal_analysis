# %%

from ucimlrepo import fetch_ucirepo
  
# fetch dataset 
air_quality = fetch_ucirepo(id=360) 
  
# data (as pandas dataframes) 
X = air_quality.data.features 
y = air_quality.data.targets 
  
# metadata 
print(air_quality.metadata) 
  
# variable information 
print(air_quality.variables) 


# %%

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Example mask
mask = X['CO(GT)'] != -200

fig, ax = plt.subplots(figsize=(6, 5))

ax.grid(which='major', linestyle='--', color='gray', linewidth=0.7)
ax.plot(X.index[mask], X['CO(GT)'][mask], color='black')
ax.set_ylabel("$mg/m^3$")

# Pick 3 evenly spaced dates from the masked index
dates_to_show = X.index[mask][[0, len(X.index[mask])//2, -1]]
ax.set_xticks(dates_to_show)

# Optional: format dates nicely if X.index is datetime
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))

plt.savefig(f"../doc/assets/diagrams/air_quality/signal.png", dpi=300)

plt.show()


# %% Diagrams

from recurrence_plot import recurrence_plot_custom, recurrence_plot
from render_plot import render_recurrence_plot

f: list[float] = list(X['CO(GT)'][::20].squeeze().tolist())
f = f / np.max(f)

path = '../doc/assets/diagrams/air_quality/'

s, plot = recurrence_plot_custom(f, D=2, p=0.1, d=1, ord=2)
img = render_recurrence_plot(s, plot)
plt.imshow(img)

img.save(path + 'a.png')
s, plot = recurrence_plot_custom(f, D=2, p=0.25, d=1, ord=2)
img = render_recurrence_plot(s, plot)
img.save(path + 'b.png')

s, plot = recurrence_plot_custom(f, D=2, p=0.5, d=1, ord=2)
img = render_recurrence_plot(s, plot)
img.save(path + 'c.png')