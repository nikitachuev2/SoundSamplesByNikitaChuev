import math
import pygame
import os
import time

# Параметры симуляции
STEP_SIZE = 0.4
STEP_DELAY = 0.2
MAX_DISTANCE = 5.0
COLLISION_THRESHOLD = 0.4
VOLUME_SMOOTHING = 0.1

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

sound_file_path = 'enhanced_wall.wav'
if not os.path.exists(sound_file_path):
    print(f"Error: The sound file '{sound_file_path}' does not exist!")
    exit()

try:
    sound = pygame.mixer.Sound(sound_file_path)
except pygame.error as e:
    print(f"Error loading sound: {e}")
    exit()

class Person:
    def __init__(self, x, y, orientation_deg):
        self.x = x
        self.y = y
        self.orientation = math.radians(orientation_deg)
        self.last_volume = 0.0

    def move_forward(self):
        self.x += STEP_SIZE * math.cos(self.orientation)
        self.y += STEP_SIZE * math.sin(self.orientation)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def calculate_distance(person, obstacle):
    dx = obstacle.x - person.x
    dy = obstacle.y - person.y
    return math.hypot(dx, dy)

def update_volume(person, distance):
    if distance > MAX_DISTANCE:
        target_volume = 0.0
    else:
        target_volume = max(0.0, 1.0 - distance / MAX_DISTANCE)

    # Плавное увеличение громкости
    volume = person.last_volume + (target_volume - person.last_volume) * VOLUME_SMOOTHING
    person.last_volume = volume
    sound.set_volume(volume)

def simulate_collision(person, obstacle, steps=100):
    print("▶ Старт симуляции")
    sound.play(-1)  # Бесконечный цикл

    for step in range(steps):
        print(f"\nШаг {step + 1}")
        distance = calculate_distance(person, obstacle)
        print(f"Расстояние до объекта: {distance:.2f}")

        if distance <= COLLISION_THRESHOLD:
            print("⚠ Столкновение! Звук продолжает играть на 100% громкости.")
            sound.set_volume(1.0)  # Максимальная громкость
            while True:
                time.sleep(1)  # Ждём бесконечно, пока пользователь не закроет программу
            break

        person.move_forward()
        update_volume(person, distance)
        time.sleep(STEP_DELAY)

    # Это никогда не выполнится при столкновении
    sound.stop()
    print("🟢 Завершено")

# Пример
person = Person(0, 2, 0)  # Идёт прямо
obstacle = Obstacle(5, 2)  # Стена прямо по курсу

simulate_collision(person, obstacle)