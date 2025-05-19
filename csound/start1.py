import ctcsound
import os
import wave
import numpy as np
import time
from scipy.io.wavfile import write
from scipy.signal import resample

def convert_wav(input_path, output_path):
    with wave.open(input_path, 'rb') as wav:
        channels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        framerate = wav.getframerate()
        frames = wav.getnframes()
        audio_data = wav.readframes(frames)

    dtype = {1: np.int8, 2: np.int16, 4: np.int32}.get(sampwidth)
    if dtype is None:
        raise ValueError("Unsupported sample width")

    audio = np.frombuffer(audio_data, dtype=dtype)

    if channels == 2:
        audio = audio.reshape(-1, 2)
        audio = audio.mean(axis=1).astype(np.int16)
    else:
        audio = audio.astype(np.int16)

    if framerate != 44100:
        audio = resample(audio, int(len(audio) * 44100 / framerate)).astype(np.int16)

    write(output_path, 44100, audio)

def collision_simulation():
    original = "myfile.wav"
    fixed = "myfile_csound.wav"

    if not os.path.exists(original):
        raise FileNotFoundError("Файл myfile.wav не найден!")

    convert_wav(original, fixed)

    csd = f'''
<CsoundSynthesizer>
<CsOptions>
-odac -d
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

gkvol chnexport "vol", 1
gkvol init 0.3
gkpan chnexport "pan", 1
gkpan init 0.0

instr 1
    a1 diskin2 "{fixed}", 1, 0, 1
    a1 = a1 * gkvol
    aL, aR pan2 a1, gkpan
    outs aL, aR
endin
</CsInstruments>
<CsScore>
i1 0 3600
</CsScore>
</CsoundSynthesizer>
'''

    cs = ctcsound.Csound()
    cs.compileCsdText(csd)
    cs.start()

    try:
        for step in range(25):
            distance = max(0.05, 5.0 - step * 0.2)
            vol = min(1.0, 1.5 / distance)
            pan = 0.0

            print(f"[{step+1}] dist={distance:.2f}  vol={vol:.2f}  pan={pan:.2f}")
            cs.setControlChannel("vol", vol)
            cs.setControlChannel("pan", pan)
            time.sleep(0.3)

            if distance < 0.4:
                print("💥 Столкновение! Зацикливаем звук...")
                for _ in range(40):
                    cs.setControlChannel("vol", 1.0)
                    cs.setControlChannel("pan", 0.0)
                    time.sleep(0.3)
                break

    finally:
        cs.stop()
        cs.cleanup()

if __name__ == "__main__":
    collision_simulation()
