# %%

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from src.equalizer import eq
from src.fft import cooley_tukey_fft

# %%

y, sr = librosa.load("data/c-e-g.m4a", sr=None)

total_time = len(y) / sr
ts = np.arange(0, total_time, 1 / sr)

plt.figure(figsize=(6, 4))
plt.plot(ts, y)

plt.xlabel("Laikas (sekundės)")
plt.ylabel("Amplitudė")
plt.title("Audio signalas (C-E-G natos)")

plt.grid(True)

plt.savefig("doc/assets/diagrams/ceg-sound.png", dpi=300, bbox_inches="tight")

# %%

def extend_sig(y):
  N = len(y)

  # check if signal extension is needed
  if N & (N - 1) == 0:
    # len is already power of 2
    return y

  new_N = 1 << N.bit_length()
  y_padded = np.zeros(new_N)
  y_padded[:N] = y
  return y_padded

# %%

from src.fft import cooley_tukey_fft

y_padded = extend_sig(y)


# %%
N = len(y_padded)
freqs = np.fft.fftfreq(N, d=1/sr)
YS = cooley_tukey_fft(y_padded)

note_freqs = {
  'C': 130.81,
  'E': 164.81,
  'G': 196.00
}

mask = (freqs >= 0) & (freqs <= 500)
amplitude = np.abs(YS) / N
amplitude[1:N//2] *= 2

plt.figure(figsize=(6, 4))

plt.plot(freqs[mask], amplitude[mask])

plt.axvline(x=note_freqs['C'], color='r', linestyle='--', label='C')
plt.axvline(x=note_freqs['E'], color='r', linestyle='--', label='E')
plt.axvline(x=note_freqs['G'], color='r', linestyle='--', label='G')

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Garso signalo dažnių spektras (C-E-G natos)")

plt.legend()
plt.grid(True)

plt.savefig("doc/assets/diagrams/ceg-spectral.png", dpi=300, bbox_inches="tight")

# %%

import soundfile as sf
from src.equalizer import eq


def gain(f):
    center = 130.81
    width = 15
    return 1 + 10 * np.exp(-((f - center)**2) / (2 * width**2))

f = np.arange(0, 400, 1)

plt.figure(figsize=(6, 4))
plt.plot(f, gain(f), label="Stiprinimo kreivė")

# C note marker
plt.axvline(x=130.81, color='r', linestyle='--', label='C (130.81 Hz)')

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Stiprinimo koeficientas")
plt.title("Ekvalaizerio stiprinimo funkcija")

plt.legend()
plt.grid(True)

plt.savefig("doc/assets/diagrams/eq-gain.png", dpi=300, bbox_inches="tight")
# %%
new_y = eq(y_padded, sr, gain)
sf.write('data/c-e-g-c-gain.wav', np.real(new_y), sr)

# %%

# time axis in seconds
t = np.arange(len(y_padded)) / sr

# mask: only first 8 seconds
mask = t <= 8

plt.figure(figsize=(6, 4))

plt.plot(t[mask], y_padded[mask], label="Pradinis signalas", alpha=0.7)
plt.plot(t[mask], np.real(new_y)[mask], label="Po ekvalaizerio", alpha=0.7)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalo prieš ir po ekvalaizerio (0–8 s)")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('doc/assets/diagrams/eq-applied.png', dpi=300, bbox_inches="tight")

# %%

import soundfile as sf
from src.equalizer import eq


def gain(f):
    center = 130.81
    width = 30
    return 1 + 10 * np.exp(-((f - center)**2) / (2 * width**2))

f = np.arange(0, 400, 1)

plt.figure(figsize=(6, 4))
plt.plot(f, gain(f), label="Stiprinimo kreivė")

# C note marker
plt.axvline(x=130.81, color='r', linestyle='--', label='C (130.81 Hz)')

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Stiprinimo koeficientas")
plt.title("Ekvalaizerio stiprinimo funkcija")

plt.legend()
plt.grid(True)

plt.savefig("doc/assets/diagrams/eq-gain-wide.png", dpi=300, bbox_inches="tight")

# %%

new_y = eq(y_padded, sr, gain)

# time axis in seconds
t = np.arange(len(y_padded)) / sr

# mask: only first 8 seconds
mask = t <= 8

plt.figure(figsize=(6, 4))

plt.plot(t[mask], y_padded[mask], label="Pradinis signalas", alpha=0.7)
plt.plot(t[mask], np.real(new_y)[mask], label="Po ekvalaizerio", alpha=0.7)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalo prieš ir po ekvalaizerio (0–8 s)")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('doc/assets/diagrams/eq-applied-wide.png', dpi=300, bbox_inches="tight")

# %% Augment melody

filename = librosa.example('trumpet')
y_noise, sr_noise = librosa.load(filename)
y, sr = librosa.load("data/melody.wav", sr=None)
y_noise_resampled = librosa.resample(y_noise, orig_sr=sr_noise, target_sr=sr)

common_len = min(len(y), len(y_noise_resampled))

y_noise_resampled = y_noise_resampled[:common_len]
y = y[:common_len]

y_noisy = y_noise_resampled + y

plt.plot(y_noisy)
sf.write('data/melody_noise.wav', np.real(y_noisy), sr)

# %%

y_padded = extend_sig(y)
N = len(y_padded)
freqs = np.fft.fftfreq(N, d=1/sr)
YS = cooley_tukey_fft(y_padded)
mask = (freqs >= 0) & (freqs <= 500)
amplitude = np.abs(YS) / N
amplitude[1:N//2] *= 2

plt.figure(figsize=(6, 4))

plt.plot(freqs[mask], amplitude[mask])

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")

plt.legend()
plt.grid(True)

# %%

def gain(f):
    return 0.0 if f > 300 else 1.0

# f = np.arange(0, 400, 1)

# plt.figure(figsize=(6, 4))
# plt.plot(f, gain(f), label="Stiprinimo kreivė")

# %%

y_recovered = eq(y_padded, sr, gain)


plt.plot(y)
plt.plot(y_recovered)



sf.write('data/melody_recovered.wav', np.real(y_recovered), sr)