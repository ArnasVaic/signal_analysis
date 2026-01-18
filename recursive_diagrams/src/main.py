# %%

from math import pi, sin

from recurrence_plot import recurrence_plot_custom
from render_plot import render_recurrence_plot

x0 = 0.51
f = [ x0 ] * 401
for i in range(400):
  f[i + 1] = 4 * f[i] * (1 - f[i])

# f = [ sin(2 * pi * x / 100) for x in range(401) ]

s, plot = recurrence_plot_custom(f, D=5, p=0.5, d=5)

img = render_recurrence_plot(s, plot)

img.save("plot.png")
