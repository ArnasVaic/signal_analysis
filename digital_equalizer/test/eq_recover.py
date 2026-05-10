# %% Importai

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from src.equalizer import eq
from src.fft import cooley_tukey_fft


# %% Grafiku stilius

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
    """
    Papildo signalą iki artimiausio 2 laipsnio ilgio.
    """

    N = len(y)

    if N & (N - 1) == 0:
        return y

    new_N = 1 << N.bit_length()

    y_padded = np.zeros(new_N)
    y_padded[:N] = y

    return y_padded


def generate_tone_noise(freq, sr, duration, amplitude=0.2):
    """
    Sugeneruoja sinusinį triukšmą.
    """

    t = np.arange(0, duration, 1 / sr)

    noise = amplitude * np.sin(
        2 * np.pi * freq * t
    )

    return noise


def compute_fft(y, sr):

    y_padded = extend_sig(y)

    N = len(y_padded)

    YS = cooley_tukey_fft(y_padded)

    freqs = np.fft.fftfreq(N, d=1 / sr)

    amplitude = np.abs(YS) / N
    amplitude[1:N // 2] *= 2

    return freqs, amplitude


# %% Užkraunama melodija

melody_sig, melody_sr = librosa.load(
    "data/melody.wav",
    sr=None
)

duration = len(melody_sig) / melody_sr

print(f"Diskretizavimo dažnis: {melody_sr} Hz")
print(f"Trukmė: {duration:.2f} s")


# %% Originalios melodijos grafikas

t = np.arange(len(melody_sig)) / melody_sr

mask_time = t <= 3

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    melody_sig[mask_time]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Originali gitaros melodija")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/melody-original-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Originalios melodijos spektras

freqs, amplitude = compute_fft(
    melody_sig,
    melody_sr
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
    "doc/assets/diagrams/melody-original-spectrum.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Generuojamas dirbtinis triukšmas

noise_freqs = [
    1000,
    2500,
    5000
]

noise_signal = np.zeros_like(melody_sig)

for freq in noise_freqs:

    noise_signal += generate_tone_noise(
        freq=freq,
        sr=melody_sr,
        duration=duration,
        amplitude=0.08
    )


# %% Triukšmo signalas

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    noise_signal[mask_time]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Sugeneruotas triukšmo signalas")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/noise-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Triukšmo spektras

freqs_noise, amplitude_noise = compute_fft(
    noise_signal,
    melody_sr
)

plt.figure(figsize=(6, 5))

plt.plot(
    freqs_noise[mask_freq],
    amplitude_noise[mask_freq]
)

for freq in noise_freqs:
    plt.axvline(
        x=freq,
        color='r',
        linestyle='--',
        label=f"{freq} Hz"
    )

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Triukšmo dažnių spektras")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/noise-spectrum.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Sukuriama triukšminga melodija

melody_noisy = melody_sig + noise_signal

# normalizavimas
melody_noisy /= np.max(
    np.abs(melody_noisy)
)

sf.write(
    "data/melody_noisy.wav",
    melody_noisy,
    melody_sr
)


# %% Triukšmingos melodijos grafikas

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    melody_noisy[mask_time]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Triukšminga gitaros melodija")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/melody-noisy-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Triukšmingos melodijos spektras

freqs_noisy, amplitude_noisy = compute_fft(
    melody_noisy,
    melody_sr
)

plt.figure(figsize=(6, 5))

plt.plot(
    freqs_noisy[mask_freq],
    amplitude_noisy[mask_freq]
)

for freq in noise_freqs:
    plt.axvline(
        x=freq,
        color='r',
        linestyle='--',
        label=f"{freq} Hz"
    )

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Triukšmingos melodijos dažnių spektras")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/melody-noisy-spectrum.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Ekvalaizerio stiprinimo funkcija

def gain(f):

    # gain_value = 1.0

    # notch_width = 160

    # for center in noise_freqs:

    #     attenuation = np.exp(
    #         -((f - center) ** 2) /
    #         (2 * notch_width ** 2)
    #     )

    #     gain_value *= (
    #         1 - attenuation
    #     )

    # return gain_value

    # alt

    # return 0.0 if f > 900 else 1.0
        

    if (f > 900 and f < 1100) or (f > 2400 and f < 2600) or (f > 4900 and f < 5100):
        return 0.0

    return 1.0


# %% Ekvalaizerio kreivė

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

for freq in noise_freqs:
    plt.axvline(
        x=freq,
        color='r',
        linestyle='--',
        label=f"{freq} Hz"
    )

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Stiprinimo koeficientas")
plt.title("Ekvalaizerio slopinimo funkcija")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/eq-function.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Taikomas ekvalaizeris

melody_noisy_padded = extend_sig(
    melody_noisy
)

melody_recovered = eq(
    melody_noisy_padded,
    melody_sr,
    gain
)

melody_recovered = np.real(
    melody_recovered
)

melody_recovered = melody_recovered[
    :len(melody_sig)
]

# normalizavimas
melody_recovered /= np.max(
    np.abs(melody_recovered)
)

sf.write(
    "data/melody_recovered.wav",
    melody_recovered,
    melody_sr
)


# %% Atkurto signalo grafikas

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    melody_recovered[mask_time]
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Melodija po triukšmo šalinimo")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/melody-recovered-time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Atkurto signalo spektras

mask_freq = (
    (freqs >= 0) &
    (freqs <= 6000)
)

freqs_recovered, amplitude_recovered = compute_fft(
    melody_recovered,
    melody_sr
)

plt.figure(figsize=(6, 5))

plt.plot(
    freqs_noisy[mask_freq],
    amplitude_noisy[mask_freq],
    label="Prieš filtravimą",
    alpha=0.7
)

plt.plot(
    freqs_recovered[mask_freq],
    amplitude_recovered[mask_freq],
    label="Po filtravimo",
    alpha=0.9
)

for freq in noise_freqs:
    plt.axvline(
        x=freq,
        color='r',
        linestyle='--',
        alpha=0.4
    )
    break

plt.xlabel("Dažnis (Hz)")
plt.ylabel("Amplitudė")
plt.title("Dažnių spektras prieš ir po filtravimo")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/recovered-spectrum.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# %% Visų signalų palyginimas laiko srityje

plt.figure(figsize=(6, 5))

plt.plot(
    t[mask_time],
    melody_noisy[mask_time],
    label="Triukšminga melodija",
    alpha=0.6
)

plt.plot(
    t[mask_time],
    melody_recovered[mask_time],
    label="Atkurta melodija",
    alpha=0.8
)

plt.plot(
    t[mask_time],
    melody_sig[mask_time],
    label="Originali melodija",
    alpha=0.8
)

plt.xlabel("Laikas (s)")
plt.ylabel("Amplitudė")
plt.title("Signalų palyginimas")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "doc/assets/diagrams/all-signals-comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# %%