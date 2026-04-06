# %%

import librosa
import matplotlib.pyplot as plt
import numpy as np
from src.equalizer import eq

y, sr = librosa.load("data/c-e-g.m4a", sr=None)

print(y.shape)  # (num_samples,)
print(sr)       # sample rate (e.g., 44100)

# sample rate is samples/s 
# how many seconds in total?
# samples * s/samples = samples / sample_rate

total_time = len(y) / sr
ts = np.arange(0, total_time, 1 / sr)

plt.plot(ts, y)

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
plt.plot(freqs[mask], amplitude[mask])
plt.axvline(x=note_freqs['C'], color='r', linestyle='--')
plt.axvline(x=note_freqs['E'], color='r', linestyle='--')
plt.axvline(x=note_freqs['G'], color='r', linestyle='--')


# %%

import soundfile as sf
from src.equalizer import eq

def gain(f):
  center = 130.81
  width = 15
  
  return 1 + 10 * np.exp(-((f - center)**2) / (2 * width**2))
  

plt.plot(gain(np.arange(0, 400, 1)))

# %%
new_y = eq(y_padded, sr, gain)
sf.write('data/c-e-g-c-gain.wav', np.real(new_y), sr)

plt.plot(np.real(new_y))
plt.plot(y_padded)

# plt.plot(np.imag(new_y))
