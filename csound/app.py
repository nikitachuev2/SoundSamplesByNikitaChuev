import ctcsound
import os
import math
import time

# ==== Настройка звука ====
wav_path = "myfile.wav"
if not os.path.isfile(wav_path):
    raise FileNotFoundError(f"Файл {wav_path} не найден!")

# ==== Симуляция движения ====
class Person:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = math.radians(orientation)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ==== Csound код с управляющими каналами ====
csd_text = f'''
<CsoundSynthesizer>
<CsOptions>
-odac
-d
</CsOptions>

<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    kpan chnget "pan"
    kgain chnget "gain"
    a1 diskin2 "{wav_path}", 1, 0, 1
    a1 = a1 * kgain
    aL, aR pan2 a1, kpan
    outs aL, aR
endin
</CsInstruments>

<CsScore>
i 1 0 -1
</CsScore>
</CsoundSynthesizer>
'''

# ==== Инициализация Csound ====
cs = ctcsound.Csound()
cs.setOption("-odac")
cs.compileCsdText(csd_text)
cs.start()

# ==== Установка начальных значений ====
cs.setControlChannel("pan", 0.0)
cs.setControlChannel("gain", 0.1)

# ==== Симуляция шагов ====
def simulate_walking(person, obstacle, steps=50, step_size=0.3):
    for step in range(steps):
        # Обновление позиции
        person.x += step_size * math.cos(person.orientation)
        person.y += step_size * math.sin(person.orientation)

        # Расчёт расстояния и угла
        dx = obstacle.x - person.x
        dy = obstacle.y - person.y
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)

        # Пространственный звук
        pan = max(-1.0, min(1.0, math.sin(angle)))  # -1 = влево, 1 = вправо
        gain = max(0.0, min(1.0, 1 / (distance + 0.5)))  # Чем ближе, тем громче

        cs.setControlChannel("pan", pan)
        cs.setControlChannel("gain", gain)

        print(f"Step {step+1}: Pos=({person.x:.2f}, {person.y:.2f}) | Distance={distance:.2f} | Pan={pan:.2f} | Gain={gain:.2f}")

        if distance < 0.5:
            print("💥 Столкновение! Звук зациклен.")
            # Симуляция зацикливания: можно просто оставить звук играть в одной точке
            for _ in range(100):  # 100 итераций "врезания"
                cs.setControlChannel("gain", 1.0)
                cs.setControlChannel("pan", pan)
                time.sleep(0.05)
            break

        time.sleep(0.1)

# ==== Пример использования ====
person = Person(0, 0, 0)  # Идёт вправо
obstacle = Obstacle(3, 0)

simulate_walking(person, obstacle)

# ==== Завершение ====
cs.stop()
cs.cleanup()
 