import math
import time
import csnd6

STEP_SIZE = 0.4
STEP_DELAY = 0.2
MAX_DISTANCE = 5.0
COLLISION_THRESHOLD = 0.4
AVOIDANCE_ANGLE = 45
VOLUME_SMOOTHING = 0.1

class Person:
    def __init__(self, x, y, orientation_deg):
        self.x = x
        self.y = y
        self.orientation = math.radians(orientation_deg)
        self.last_volume = 0.0

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

def simulate_navigation(person, obstacles, cs):
    print("▶ Старт симуляции через Csound...")

    for step in range(80):
        print(f"\nШаг {step + 1}")
        nearest_obstacle = None
        nearest_distance = float('inf')
        nearest_angle = 0

        for obs in obstacles:
            dist, angle = calculate_distance_and_angle(person, obs)
            if dist < nearest_distance:
                nearest_obstacle = obs
                nearest_distance = dist
                nearest_angle = angle

        print(f"Расстояние: {nearest_distance:.2f}, Угол: {nearest_angle:.2f}")

        if nearest_distance < COLLISION_THRESHOLD:
            print("❌ Столкновение!")
            break

        if abs(nearest_angle) > AVOIDANCE_ANGLE and nearest_distance < MAX_DISTANCE:
            turn = -10 if nearest_angle > 0 else 10
            print(f"↪ Обход: поворот на {turn}°")
            person.rotate(turn)

        person.move_forward()

        # Плавное изменение громкости
        target_volume = max(0.0, 1.0 - nearest_distance / MAX_DISTANCE) if nearest_distance < MAX_DISTANCE else 0.0
        person.last_volume += (target_volume - person.last_volume) * VOLUME_SMOOTHING

        # Передача значения громкости в Csound
        cs.SetChannel("volume", person.last_volume)

        time.sleep(STEP_DELAY)

    print("🟢 Навигация завершена.")

# Настройка и запуск Csound
cs = csnd6.Csound()
cs.Compile("wall.orc")
perf_thread = csnd6.CsoundPerformanceThread(cs)
perf_thread.Play()

# Объекты и симуляция
person = Person(0, 2, -30)
obstacles = [Obstacle(5, 2)]
simulate_navigation(person, obstacles, cs)

# Завершение
perf_thread.Stop()
perf_thread.Join()