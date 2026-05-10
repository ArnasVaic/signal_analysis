# %% Imports

import librosa
import numpy as np
import matplotlib.pyplot as plt

from src.fft import cooley_tukey_fft


# %% Styling (match your report)

plt.rcParams.update({
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "legend.fontsize": 14
})


# %% Helpers

def extend_sig(y):
    N = len(y)

    if N & (N - 1) == 0:
        return y

    new_N = 1 << N.bit_length()

    y_padded = np.zeros(new_N)
    y_padded[:N] = y

    return y_padded


# %% FFT per window

def window_fft(chunk, sr):

    chunk = extend_sig(chunk)
    N = len(chunk)

    X = cooley_tukey_fft(chunk)

    freqs = np.fft.fftfreq(N, d=1/sr)

    mag = np.abs(X) / N
    mag[1:N//2] *= 2

    mask = (freqs >= 0)

    return freqs[mask], mag[mask]


# %% Load audio (use your melody or DnB)

y, sr = librosa.load(
    "data/dialup.mp3",
    sr=None
)

# optional: shorten for speed
y = y[:10 * sr]  # first 10 seconds


# %% Spectrogram parameters

window_size = 4096
hop_size = 1024

spectrogram = []
time_axis = []

# %% Build spectrogram manually

for i in range(0, len(y) - window_size, hop_size):

    chunk = y[i:i + window_size]

    f, mag = window_fft(chunk, sr)

    spectrogram.append(mag)
    time_axis.append(i / sr)

spectrogram = np.array(spectrogram).T
time_axis = np.array(time_axis)


# %% 1. LINEAR SPECTROGRAM

plt.figure(figsize=(6, 5))

plt.imshow(
    spectrogram,
    aspect="auto",
    origin="lower",
    extent=[
        time_axis[0],
        time_axis[-1],
        0,
        sr / 2
    ]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Dažnis (Hz)")
plt.title("Spektrograma (FFT laiko srityje)")

plt.colorbar(label="Amplitudė")

plt.tight_layout()
plt.savefig(
    "doc/assets/diagrams/spectrogram-linear.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# %% 2. LOG SPECTROGRAM (MUCH MORE INFORMATIVE)

plt.figure(figsize=(6, 5))

ls = 10 * np.log10(spectrogram + 1e-10)

plt.imshow(
    ls[:220,:],
    aspect="auto",
    origin="lower",
    extent=[
        time_axis[0],
        time_axis[-1],
        0,
        sr / 2
    ],
    vmin=np.min(ls),
    vmax=np.max(ls)
)

plt.xlabel("Laikas (s)")
plt.ylabel("Dažnis (Hz)")
plt.title("Spektrograma (log skalė)")

plt.colorbar(label="dB")

plt.tight_layout()
plt.savefig(
    "doc/assets/diagrams/spectrogram-log.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# %% 3. TIME DOMAIN REFERENCE

t = np.arange(len(y)) / sr
mask = t <= 5

plt.figure(figsize=(6, 5))

plt.plot(t[mask], y[mask])

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalo forma laiko srityje")

plt.grid(True)

plt.tight_layout()
plt.savefig(
    "doc/assets/diagrams/spectrogram-time.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()