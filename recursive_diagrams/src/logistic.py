# %%

from math import pi, sin

from recurrence_plot import recurrence_plot
from render_plot import render_recurrence_plot

x0 = 0.51
N = 400
f = [ x0 ] * (N + 1)
for i in range(400):
  f[i + 1] = 4 * f[i] * (1 - f[i])

s, plot = recurrence_plot(f, D=2, r=0.1 , d=1)
img = render_recurrence_plot(s, plot)
img.save("../doc/assets/diagrams/logistic/a.png")

s, plot = recurrence_plot(f, D=2, r=0.5 , d=1)
img = render_recurrence_plot(s, plot)
img.save("../doc/assets/diagrams/logistic/b.png")

# %% Plot logistic signal

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 18})  # adjust number as needed (12–18 usually works for papers)

# Example plot setup
fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(f, color='black')

ax.set_xticks([0, 100, 200, 300, 400])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])

ax.xaxis.set_minor_locator(ticker.LinearLocator(numticks=20))  # 4 minor ticks between majors
ax.yaxis.set_minor_locator(ticker.LinearLocator(numticks=20))  # 3 minor ticks between majors

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)

ax.grid(which='major', linestyle='--', color='gray', linewidth=0.7)

# Tight layout for clean spacing
plt.tight_layout()

# Save figure for paper
plt.savefig("../doc/assets/diagrams/logistic/c.png", dpi=300)     # vector PDF, good for print
# plt.savefig("figure1.png", dpi=600)   # alternative: high-res raster image

plt.show()

