# %% Importai

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from src.equalizer import eq
from src.fft import cooley_tukey_fft


# %% Grafikų stilius

plt.rcParams.update({
    "font.size": 16,
    "axes.titlesize": 20,
    "axes.labelsize": 18,
    "legend.fontsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})


# %% Pagalbinės funkcijos

def extend_sig(y):

    N = len(y)

    if N & (N - 1) == 0:
        return y

    new_N = 1 << N.bit_length()

    y_padded = np.zeros(new_N)
    y_padded[:N] = y

    return y_padded


def compute_fft(y, sr):

    y_padded = extend_sig(y)

    N = len(y_padded)

    YS = cooley_tukey_fft(y_padded)

    freqs = np.fft.fftfreq(
        N,
        d=1 / sr
    )

    amplitude = np.abs(YS) / N
    amplitude[1:N // 2] *= 2

    return freqs, amplitude


# %% Užkraunama melodija

start_time = 49
end_time = 55

y, sr = librosa.load(
    "data/rex-orange-sunflower.mp3",
    sr=None,
    offset=start_time,
    duration=end_time - start_time
)

t = np.arange(len(y)) / sr

print(f"Diskretizavimo dažnis: {sr} Hz")

sf.write(
    "data/sunflower-cut.wav",
    y,
    sr
)

# %% Originalus signalas laiko srityje

mask_time = t <= 3

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    y[mask_time]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Originali gitaros melodija")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/telephone-original-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Originalus dažnių spektras

freqs, amplitude = compute_fft(
    y,
    sr
)

mask_freq = (
    (freqs >= 0) &
    (freqs <= 6000)
)

plt.figure(figsize=(6, 5))

plt.plot(
    freqs[mask_freq],
    amplitude[mask_freq]
)

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Originalios melodijos dažnių spektras")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/telephone-original-spectrum.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Telefono efekto ekvalaizeris

# Paliekami tik vidutiniai dažniai:
# ~300 Hz - 3000 Hz

def gain(f):

    if 300 <= f <= 3000:
        return 1.0

    return 0.0


# %% Ekvalaizerio funkcijos grafikas

f = np.arange(0, 6000, 1)

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
    x=300,
    color='r',
    linestyle='--',
    label='300 Hz'
)

plt.axvline(
    x=3000,
    color='r',
    linestyle='--',
    label='3000 Hz'
)

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Stiprinimo koeficientas")
plt.title("Telefono efekto filtravimo funkcija")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/telephone-gain.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Taikomas telefono efektas

y_padded = extend_sig(y)

y_telephone = eq(
    y_padded,
    sr,
    gain
)

y_telephone = np.real(
    y_telephone
)

# pašalinamas padding
y_telephone = y_telephone[:len(y)]

# normalizavimas
y_telephone /= np.max(
    np.abs(y_telephone)
)

sf.write(
    "data/melody-telephone.wav",
    y_telephone,
    sr
)


# %% Signalo palyginimas laiko srityje

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    y[mask_time],
    label="Originali melodija",
    alpha=0.8
)

plt.plot(
    t[mask_time],
    y_telephone[mask_time],
    label="Telefono efektas",
    alpha=0.8
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalas prieš ir po telefono efekto")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/telephone-time-comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Dažnių spektro palyginimas

freqs_tel, amplitude_tel = compute_fft(
    y_telephone,
    sr
)

plt.figure(figsize=(6, 5))

plt.plot(
    freqs[mask_freq],
    amplitude[mask_freq],
    label="Originali melodija",
    alpha=0.7
)

plt.plot(
    freqs_tel[mask_freq],
    amplitude_tel[mask_freq],
    label="Telefono efektas",
    alpha=0.9
)

plt.axvline(
    x=300,
    color='r',
    linestyle='--'
)

plt.axvline(
    x=3000,
    color='r',
    linestyle='--'
)

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Dažnių spektras prieš ir po filtravimo")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/telephone-spectrum-comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()