import numpy as np
from scipy.io.wavfile import write

sr = 44100
duration = 2.0

t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Low electric hum
hum = np.sin(2 * np.pi * (120 + 3*np.sin(2*np.pi*5*t)) * t)

# Soft buzz
buzz = 0.18 * np.sin(2 * np.pi * 700 * t)
buzz *= 0.5 + 0.5*np.sin(2*np.pi*14*t)

# Sliding air
noise = np.random.normal(0, 1, len(t))

# Smooth the noise (low-pass)
kernel = np.ones(120) / 120
noise = np.convolve(noise, kernel, mode="same")

# Make the noise pulse slightly
noise *= (0.4 + 0.6*np.sin(2*np.pi*4*t)**2)

# High shimmer
shine = 0.08 * np.sin(2*np.pi*1800*t)
shine *= 0.5 + 0.5*np.sin(2*np.pi*9*t)

audio = (
    0.45 * hum +
    buzz +
    0.30 * noise +
    shine
)

# Fade
fade = int(sr * 0.02)
audio[:fade] *= np.linspace(0, 1, fade)
audio[-fade:] *= np.linspace(1, 0, fade)

# Normalize
audio /= np.max(np.abs(audio))
audio *= 0.4

write("move_slide.wav", sr, (audio * 32767).astype(np.int16))

print("Saved move_slide.wav")