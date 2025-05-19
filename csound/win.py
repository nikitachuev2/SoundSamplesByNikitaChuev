import ctcsound
import math
import os
import threading
import time
from pynput import keyboard

# === Конфигурация ===
wav_path = "myfile.wav"
obstacle_pos = (3.0, 0.0)
step_size = 0.3
hearing_radius = 1.0
collision_distance = 0.3

if not os.path.isfile(wav_path):
    raise FileNotFoundError(f"Файл {wav_path} не найден!")

position = [0.0, 0.0]
keys_pressed = set()

# === Клавиатура ===
def on_press(key):
    try:
        keys_pressed.add(key.char.lower())
    except:
        pass

def on_release(key):
    try:
        keys_pressed.discard(key.char.lower())
    except:
        pass
    if key == keyboard.Key.esc:
        return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# === CSD-инструмент Csound ===
csd = f'''
<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1

instr 1
    kpan chnget "pan"
    kgain chnget "gain"
    kloop chnget "loop"

    if kloop >= 1 then
        a1 diskin2 "{wav_path}", 1, 0, 1
    else
        a1 diskin2 "{wav_path}", 1, 0, 0
    endif

    a1 = a1 * kgain
    aL, aR pan2 a1, kpan
    outs aL, aR
endin
</CsInstruments>
<CsScore>
i 1 0 3600
</CsScore>
</CsoundSynthesizer>
'''

# === Звуковой поток ===
def csound_thread():
    cs = ctcsound.Csound()
    cs.compileCsdText(csd)
    cs.start()
    cs.setControlChannel("pan", 0)
    cs.setControlChannel("gain", 0)
    cs.setControlChannel("loop", 0)

    while True:
        dx = obstacle_pos[0] - position[0]
        dy = obstacle_pos[1] - position[1]
        distance = math.hypot(dx, dy)

        # === Пространственная панорама: от -1 до 1 ===
        pan = max(min(dx / hearing_radius, 1.0), -1.0)

        # === Усиление только в радиусе слышимости ===
        if distance <= hearing_radius:
            gain = max(0.05, 1.0 - distance / hearing_radius)
        else:
            gain = 0.0

        # === Зацикливаем звук при столкновении ===
        loop = 1 if distance < collision_distance else 0

        cs.setControlChannel("pan", pan)
        cs.setControlChannel("gain", gain)
        cs.setControlChannel("loop", loop)

        print(f"\r📍 Pos=({position[0]:.2f},{position[1]:.2f}) | Dist={distance:.2f} | Gain={gain:.2f} | Pan={pan:.2f} | {'💥 collision' if loop else '🟢'}", end='')
        cs.performKsmps()
        time.sleep(0.01)

cs_thread = threading.Thread(target=csound_thread, daemon=True)
cs_thread.start()

# === Движение ===
print("\n🕹 Управление: W - вверх, S - вниз, A - влево, D - вправо. Esc — выход.")
try:
    while True:
        if 'w' in keys_pressed:
            position[1] += step_size
        if 's' in keys_pressed:
            position[1] -= step_size
        if 'a' in keys_pressed:
            position[0] -= step_size
        if 'd' in keys_pressed:
            position[0] += step_size
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

print("\n🚪 Выход.")
 