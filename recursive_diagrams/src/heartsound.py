# %%

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from PIL import Image

from recurrence_plot import recurrence_plot_custom, recurrence_plot
from render_plot import render_recurrence_plot

sample_rate, data = wavfile.read("../data/HS/M_N_RUSB.wav")

# %%

plt.rcParams.update({'font.size': 16})

# Create figure (slightly rectangular, adjust if you want square)
fig, ax = plt.subplots(figsize=(6, 5))

sig = data / data.max()
t = np.arange(len(sig)) / sample_rate
ax.grid(which='major', linestyle='--', color='gray', linewidth=0.7)
ax.set_xlim(t[0], t[-1]+0.01)
ax.plot(t, sig, color='black')
ax.set_xlabel("Laikas (s)")
ax.set_ylabel("Amplitudė")
fig.tight_layout()
plt.savefig(f"../doc/assets/diagrams/heart_sound/signal.png", dpi=300)


plt.show()

# %%

f: list[float] = list(data[::100])
f = f / np.max(f)

path = '../doc/assets/diagrams/heart_sound/'

s, plot = recurrence_plot_custom(f, D=2, p=0.1, d=2, ord=2)
img = render_recurrence_plot(s, plot)
plt.imshow(img)

img.save(path + 'a.png')
s, plot = recurrence_plot_custom(f, D=2, p=0.1, d=5, ord=2)
img = render_recurrence_plot(s, plot)
img.save(path + 'b.png')

s, plot = recurrence_plot_custom(f, D=2, p=0.1, d=7, ord=2)
img = render_recurrence_plot(s, plot)
img.save(path + 'c.png')