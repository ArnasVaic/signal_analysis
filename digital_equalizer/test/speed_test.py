# %%

import numpy as np
import matplotlib.pyplot as plt
from src.dft import dft
from src.fft import cooley_tukey_fft
import time

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

def benchmark_algorithms(y, sr, max_seconds=0.05, num_points=10):
    lengths_sec = np.linspace(0.0001, max_seconds, num_points)

    dft_times = []
    fft_times = []
    actual_lengths = []

    for sec in lengths_sec:
        N = int(sec * sr)
        if N < 2:
            continue

        signal = y[:N]

        # --- DFT (NO padding) ---
        start = time.perf_counter()
        _ = dft(signal)
        dft_time = time.perf_counter() - start

        # --- FFT (pad to power of 2) ---
        padded = extend_sig(signal)

        start = time.perf_counter()
        _ = cooley_tukey_fft(padded)
        fft_time = time.perf_counter() - start

        dft_times.append(dft_time)
        fft_times.append(fft_time)
        actual_lengths.append(len(signal) / sr)

        print(f"N={len(signal)} | DFT: {dft_time:.4f}s | FFT: {fft_time:.4f}s")

    return actual_lengths, dft_times, fft_times

# %%

import librosa
y, sr = librosa.load("data/c-e-g.m4a", sr=None)

lengths, dft_times, fft_times = benchmark_algorithms(y, sr)


# %%


plt.figure()
plt.plot(lengths, dft_times, label="Klasikinis DFT")
plt.plot(lengths, fft_times, label="Cooley-Tukey FFT")

plt.xlabel("Signalo laikas (sekundės)")
plt.ylabel("Algoritmo laikas (sekundės)")
plt.title("DFT/FFT Vykdymo laiko palyginimas")
plt.legend()
plt.grid()
plt.yscale("log")

plt.show()