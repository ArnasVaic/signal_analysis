# %% Importai

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from src.equalizer import eq


# %% Grafikų stilius

plt.rcParams.update({
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "legend.fontsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})


# %% Pagalbinė funkcija

def extend_sig(y):

    N = len(y)

    if N & (N - 1) == 0:
        return y

    new_N = 1 << N.bit_length()

    y_padded = np.zeros(new_N)
    y_padded[:N] = y

    return y_padded


# %% Užkraunamas tik reikalingas fragmentas

start_time = 2 * 60 + 9   # 2:09
end_time = 2 * 60 + 19    # 2:19

y, sr = librosa.load(
    "data/dnb.mp3",
    sr=None,
    offset=start_time,
    duration=end_time - start_time
)

t = np.arange(len(y)) / sr

sf.write(
    "data/dnb-cut.wav",
    y,
    sr
)

# %% Bass boost stiprinimo funkcija

def gain(f):

    center = 120
    width = 120

    return 1 + 3 * np.exp(
        -((f - center) ** 2) /
        (2 * width ** 2)
    )


# %% Stiprinimo funkcijos grafikas

f = np.arange(0, 2000, 1)

gain_values = np.array([
    gain(freq)
    for freq in f
])

plt.figure(figsize=(6, 5))

plt.plot(
    f,
    gain_values,
    linewidth=3
)

plt.axvline(
    x=120,
    color='r',
    linestyle='--',
    label='120 Hz'
)

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Stiprinimo koeficientas")
plt.title("Bass boost stiprinimo funkcija")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/bass-boost-gain.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Taikomas bass boost

y_padded = extend_sig(y)

y_boosted = eq(
    y_padded,
    sr,
    gain
)

y_boosted = np.real(y_boosted)

# pašalinamas padding
y_boosted = y_boosted[:len(y)]

# normalizavimas
y_boosted /= np.max(np.abs(y_boosted))

sf.write(
    "data/dnb-bass-boost.wav",
    y_boosted,
    sr
)


# %% Signalo palyginimas

mask = t <= 3

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask],
    y_boosted[mask],
    label="Bass boost",
    alpha=0.8
)

plt.plot(
    t[mask],
    y[mask],
    label="Originalus signalas",
    alpha=0.8
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalas prieš ir po bass boost")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/bass-boost-comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# %%