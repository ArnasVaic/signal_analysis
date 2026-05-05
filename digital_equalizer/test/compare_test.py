# %%
import numpy as np

N = 16
t = np.arange(N)

# mixture of two sine waves
signal = (
    np.sin(2 * np.pi * 2 * t / N) +
    0.5 * np.sin(2 * np.pi * 4 * t / N)
)

# %%
from scipy.fft import fft as scipy_fft
import matplotlib.pyplot as plt
from src.fft import cooley_tukey_fft

signal = signal.astype(np.complex128)

# Your FFT
my_fft = cooley_tukey_fft(signal)

# Reference FFT (SciPy)
ref_fft = scipy_fft(signal)

# --- Error metrics ---
my_fft = np.array(cooley_tukey_fft(signal), dtype=np.complex128)
ref_fft = np.array(scipy_fft(signal), dtype=np.complex128)
abs_error = np.abs(my_fft - ref_fft)
max_error = np.max(abs_error)
mean_error = np.mean(abs_error)

print(f"Max error: {max_error:.6e}")
print(f"Mean error: {mean_error:.6e}")

# %%

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(np.real(my_fft), 'o-', label="Mano FFT")
plt.plot(np.real(ref_fft), 'x--', label="SciPy FFT")
plt.title("Realioji dalis")
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(np.imag(my_fft), 'o-', label="Mano FFT")
plt.plot(np.imag(ref_fft), 'x--', label="SciPy FFT")
plt.title("Menamoji dalis")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# %%

plt.figure()

plt.stem(np.abs(my_fft), linefmt='b-', markerfmt='bo', basefmt=" ", label="Mano FFT")
plt.stem(np.abs(ref_fft), linefmt='r--', markerfmt='rx', basefmt=" ", label="SciPy FFT")

plt.title("Spektro amplitudė")
plt.xlabel("Dažnių indeksas")
plt.ylabel("Amplitudė")
plt.legend()
plt.grid()

plt.show()

# %%

plt.figure()

plt.stem(abs_error)
plt.title("Absoliuti paklaida |mano - scipy|")
plt.xlabel("Indeksas")
plt.ylabel("Klaida")
plt.grid()

plt.show()