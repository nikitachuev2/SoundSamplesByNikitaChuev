import ctcsound
import os

# Путь к твоему файлу
wav_path = "myfile.wav"

# Проверка существования
if not os.path.isfile(wav_path):
    raise FileNotFoundError(f"Файл {wav_path} не найден!")

# Csound-код адаптирован под 1-канальный WAV
csd_text = f'''
<CsoundSynthesizer>
<CsOptions>
-odac
-d
</CsOptions>

<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 1
0dbfs = 1

instr 1
    a1 diskin2 "{wav_path}", 1, 0, 1
    out a1
endin
</CsInstruments>

<CsScore>
i 1 0 10
</CsScore>
</CsoundSynthesizer>
'''

# Запуск
cs = ctcsound.Csound()
cs.setOption("-odac")
cs.compileCsdText(csd_text)
cs.start()

while cs.performKsmps() == 0:
    pass

cs.stop()
cs.cleanup()