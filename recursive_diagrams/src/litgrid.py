# %%

from contextlib import contextmanager
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from recurrence_plot import recurrence_plot_custom, recurrence_plot
from render_plot import render_recurrence_plot
import calendar

df = pd.read_excel('../data/litgrid/litgrid-2025.xls')

signal = df['fact'].squeeze().tolist()

# %% Measure speedup

@contextmanager
def timed(msg="Elapsed"):
  start = time.perf_counter()
  yield lambda: time.perf_counter() - start
  end = time.perf_counter()
  print(f"{msg}: {end - start:.6f} seconds")

f = signal[::8]

with timed("norm=inf"):
    s, plot = recurrence_plot_custom(f, D=2, p=0.3, d=1, ord='inf')


with timed("norm=manh"):
    s, plot = recurrence_plot_custom(f, D=2, p=0.3, d=1, ord=1)
    
with timed("norm=euclid"):
    s, plot = recurrence_plot_custom(f, D=2, p=0.3, d=1, ord=2)

# %%
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


# %%

import numpy as np
from PIL import Image
import matplotlib.cm as cm


def save_arr_as_png(arr, saveas):
  arr = np.flip(arr, 1)
  norm = arr / arr.max()
  cmap = cm.get_cmap("viridis")  # try: plasma, magma, inferno, cividis
  rgba = cmap(norm)
  rgb = (rgba[:, :, :3] * 255).astype(np.uint8)
  img = Image.fromarray(rgb)
  img.save(saveas)
  
save_arr_as_png(result, '../doc/assets/diagrams/energy/megadiagram.png')

def cut_day(r, x, y):
  pts_per_day = 24 * 4
  n = pts_per_day
  ox = n * x
  oy = n * y
  return r[ox : ox + n:, oy : oy + n]

r1 = cut_day(result, 7, 7)
# save_arr_as_png(r1, '../doc/assets/diagrams/energy/rd_main_diag.png')

r2 = cut_day(result, 7, 14)
# save_arr_as_png(r2, '../doc/assets/diagrams/energy/rd_off_diag.png')

# %%
import numpy as np
import matplotlib.pyplot as plt

data = r1  # shape (96, 96)

fig, ax = plt.subplots(figsize=(6.8, 6), constrained_layout=True)

im = ax.imshow(
    data,
    cmap="viridis",
    origin="lower",
    aspect="auto",
    extent=[0, 96, 0, 96]
)

# ---- 6-hour markings ----
steps_per_hour = 4
steps_per_6h = 6 * steps_per_hour  # 24

ticks = np.arange(0, 97, steps_per_6h)
labels = np.arange(0, 25, 6)

ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

# ---- Grid lines ----
ax.grid(
    which="major",
    color="black",
    linestyle="--",
    linewidth=0.8,
    alpha=0.7
)

# ---- Axis labels ----
ax.set_xlabel("val.", fontsize=26)
ax.set_ylabel("val.", fontsize=26)

ax.tick_params(labelsize=26, width=1.2)

# ---- Colorbar (correct way) ----
cbar = fig.colorbar(
    im,
    ax=ax,
    fraction=0.046,   # width of colorbar
    pad=0.04          # space between plot and colorbar
)

cbar.ax.tick_params(labelsize=22, width=1.2)
# Optional label:
# cbar.set_label("MW", fontsize=24)

# ---- Save & show ----
plt.savefig(
    "../doc/assets/diagrams/energy/rd_main_diag.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# %%

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

# Ensure datetime
df["time"] = pd.to_datetime(df["time"])

df_year = df
df_month = df[df["time"].dt.month == 6]

# Lithuanian month names
lt_months = {
    1: "Sausis", 2: "Vasaris", 3: "Kovas", 4: "Balandis",
    5: "Gegužė", 6: "Birželis", 7: "Liepa", 8: "Rugpjūtis",
    9: "Rugsėjis", 10: "Spalis", 11: "Lapkritis", 12: "Gruodis"
}

def lt_month_formatter(x, pos=None):
    dt = mdates.num2date(x)
    return lt_months.get(dt.month, "")

# ----------------------------
# Large fonts for print
# ----------------------------
plt.rcParams.update({
    "font.size": 18,
    "axes.labelsize": 20,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18
})

# ----------------------------
# Figure layout
# ----------------------------
fig, axes = plt.subplots(
    1, 2,
    figsize=(14, 4.5),
    constrained_layout=True
)

# ============================
# YEAR (2025)
# ============================
ax = axes[0]
ax.plot(df_year["time"], df_year["fact"], color="black", linewidth=0.8)

ax.set_ylabel("MW")
ax.set_xlabel("2025 m.")

# Quarter ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(FuncFormatter(lt_month_formatter))

# Month separators
for m in pd.date_range(
    "2025-01-01", "2025-12-31", freq="MS"
):
    ax.axvline(m, color="black", linestyle="--", linewidth=0.4, alpha=0.4)

# ============================
# MONTH (BIRŽELIS)
# ============================
ax = axes[1]
ax.plot(df_month["time"], df_month["fact"], color="black", linewidth=1.0)

ax.set_xlabel("Birželis")

# Weekly ticks
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))

# ----------------------------
# Final polish
# ----------------------------
for ax in axes:
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)

plt.savefig("../doc/assets/diagrams/energy/signal.png", dpi=300)
plt.show()
