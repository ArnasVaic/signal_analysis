import numpy as np

def extend_sig(y):
    """
    Extend signal length to nearest power of 2
    for efficient FFT computation.
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
    Generate sinusoidal noise of target frequency.
    """
    t = np.arange(0, duration, 1 / sr)

    noise = amplitude * np.sin(2 * np.pi * freq * t)

    return noise