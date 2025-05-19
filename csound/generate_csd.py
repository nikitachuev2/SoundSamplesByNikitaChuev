from scipy.io.wavfile import write
import numpy as np

rate = 44100
duration = 2  # секунды
t = np.linspace(0, duration, int(rate * duration), False)
tone = 0.5 * np.sin(2 * np.pi * 440 * t)
tone = (tone * 32767).astype(np.int16)
write("test.wav", rate, tone)
