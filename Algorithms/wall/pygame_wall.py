import math
import pygame
import os
import time

# Параметры симуляции
STEP_SIZE = 0.4
STEP_DELAY = 0.2
MAX_DISTANCE = 5.0
COLLISION_THRESHOLD = 0.4
AVOIDANCE_ANGLE = 45  # Угол, при котором активируется обход
VOLUME_SMOOTHING = 0.1  # Чем меньше, тем плавнее звук

# Инициализация Pygame и звуковой системы
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
        self.last_volume = 0.0  # для плавности изменения громкости

    def move_forward(self):
        self.x += STEP_SIZE * math.cos(self.orientation)
        self.y += STEP_SIZE * math.sin(self.orientation)

    def rotate(self, angle_deg):
        self.orientation += math.radians(angle_deg)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def calculate_distance_and_angle(person, obstacle):
    dx = obstacle.x - person.x
    dy = obstacle.y - person.y
    distance = math.hypot(dx, dy)
    angle_to_obj = math.atan2(dy, dx)
    relative_angle = (angle_to_obj - person.orientation + math.pi) % (2 * math.pi) - math.pi
    return distance, math.degrees(relative_angle)

def update_sound(person, distance):
    if distance > MAX_DISTANCE:
        target_volume = 0.0
    else:
        target_volume = max(0.0, 1.0 - distance / MAX_DISTANCE)

    # Плавное изменение громкости
    volume = person.last_volume + (target_volume - person.last_volume) * VOLUME_SMOOTHING
    person.last_volume = volume
    sound.set_volume(volume)

def simulate_navigation(person, obstacles, steps=80):
    sound.play(-1)

    for step in range(steps):
        print(f"\nStep {step + 1}")

        nearest_obstacle = None
        nearest_distance = float('inf')
        nearest_angle = 0

        # Найти ближайшее препятствие
        for obs in obstacles:
            dist, angle = calculate_distance_and_angle(person, obs)
            if dist < nearest_distance:
                nearest_obstacle = obs
                nearest_distance = dist
                nearest_angle = angle

        print(f"Distance = {nearest_distance:.2f}, Angle = {nearest_angle:.2f}")

        if nearest_distance < COLLISION_THRESHOLD:
            print("⚠ Столкновение!")
            break

        # Изменение направления при опасном угле (обход)
        if abs(nearest_angle) > AVOIDANCE_ANGLE and nearest_distance < MAX_DISTANCE:
            turn_angle = -10 if nearest_angle > 0 else 10
            print(f"↪ Обход: поворот на {turn_angle}°")
            person.rotate(turn_angle)

        person.move_forward()
        update_sound(person, nearest_distance)
        time.sleep(STEP_DELAY)

    sound.stop()
    print("🟢 Навигация завершена.")

# Пример использования
person = Person(0, 2, -30)
obstacles = [Obstacle(5, 2)]  # можно добавить больше объектов в этот список

simulate_navigation(person, obstacles)
 