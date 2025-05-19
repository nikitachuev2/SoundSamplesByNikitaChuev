import math
import ctcsound
import time
import os

class Person:
    def __init__(self, x, y, orientation_deg):
        self.x = x
        self.y = y
        self.orientation = math.radians(orientation_deg)

    def step(self, size=1.0):
        self.x += size * math.cos(self.orientation)
        self.y += size * math.sin(self.orientation)

def simulate_and_control(person, steps=20, step_size=1.0):
    cs = ctcsound.Csound()
    cs.setOption("-odac")
    cs.compileCsd("spatial_audio.csd")  # имя файла CSD
    cs.start()

    cs.readScore("i1 0 60\n")  # правильно: readScore

    for step in range(steps):
        person.step(step_size)
        cs.setControlChannel("posx", person.x)
        print(f"[{step+1}] posx: {person.x:.2f}")
        time.sleep(0.5)

    cs.stop()
    cs.cleanup()

# Запуск
if not os.path.exists("myfile.wav"):
    print("⚠️ Файл myfile.wav не найден!")
else:
    person = Person(0, 0, 20)  # стартовое направление
    simulate_and_control(person)
 
