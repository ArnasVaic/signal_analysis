# %%

import yfinance as yf
import matplotlib.pyplot as plt

from recurrence_plot import recurrence_plot_custom
from render_plot import render_recurrence_plot

# Any ticker you want
ticker = "AAPL"

# Download historical data
df = yf.download(
  ticker, 
  start='2025-01-01', 
  end='2025-12-31',
  interval="4h"
)

# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sig = np.array(df["Close"].squeeze().tolist())

# Set bigger fonts for paper
plt.rcParams.update({'font.size': 16})

# Create figure (slightly rectangular, adjust if you want square)
fig, ax = plt.subplots(figsize=(6, 5))

ax.set_xlim(df.index[0], df.index[-1])
ax.set_ylim(sig.min(), sig.max())

# Plot closing price in black, thicker line
ax.plot(df.index, sig, color='black', linewidth=1.5)

# Set x-axis major ticks: every 50 data points (adjust as needed)
# ax.set_xticks(df.index[::3 * 11 * 5 - 1])
ax.get_xaxis().set_visible(False)

# Set y-axis major ticks based on min/max rounded nicely
ymin, ymax = sig.min(), sig.max()
ax.set_yticks([
  y for y in 
  list(np.linspace(ymin, ymax, 6))
])  # 6 major ticks

# Grid: dashed at major ticks
ax.grid(which='major', linestyle='--', color='gray', linewidth=0.7)
# Optional: lighter grid at minor ticks
# ax.grid(which='minor', linestyle=':', color='lightgray', linewidth=0.5)

# Show all borders
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)

# Labels
ax.set_xlabel("Data")
ax.set_ylabel("Kaina ($)")

# Tight layout
plt.tight_layout()

# Optional: save as high-quality PDF for paper
plt.savefig(f"../doc/assets/diagrams/finance/signal.png", dpi=300)

plt.show()

# %%
f = df["Close"].squeeze().tolist()

s, plot = recurrence_plot_custom(f, D=2, p=0.1, d=1, ord=2)
img = render_recurrence_plot(s, plot)
plt.imshow(img)
img.save('../doc/assets/diagrams/finance/a.png')

# s, plot = recurrence_plot_custom(f, D=3, p=0.5, d=1, ord='inf')
# img = render_recurrence_plot(s, plot)
# img.save('../doc/assets/diagrams/finance/b.png')

s, plot = recurrence_plot_custom(f, D=5, p=0.1, d=1, ord=2)
img = render_recurrence_plot(s, plot)
img.save('../doc/assets/diagrams/finance/c.png')
