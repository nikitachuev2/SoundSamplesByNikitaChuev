
import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Walking Simulator")

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Классы для пользователя и препятствия
class Person:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = math.radians(orientation)  # Конвертируем градусы в радианы

    def move_forward(self, step_size):
        self.x += step_size * math.cos(self.orientation)
        self.y += step_size * math.sin(self.orientation)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def calculate_distance_and_angle(person, obstacle):
    dx = obstacle.x - person.x
    dy = obstacle.y - person.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.atan2(dy, dx)  # Угол в радианах
    return distance, angle

def main():
    # Загрузка звука
    wall_sound = pygame.mixer.Sound("enhanced_wall.wav")
    
    # Создание объекта пользователя и препятствия
    person = Person(0, 2, -10)  # Начальная позиция и ориентация
    obstacle = Obstacle(5, 2)  # Позиция стены
    
    # Настройка симуляции
    steps = 20
    step_size = 0.1  # Размер шага
    passing_threshold = 2  # Расстояние, при котором симуляция считается завершенной после прохода мимо
                
    for step in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Двигаем пользователя вперед
        person.move_forward(step_size)

        # Рассчитываем расстояние и угол до стены
        distance, angle = calculate_distance_and_angle(person, obstacle)
        
        # Вывод информации о текущем шаге
        print(f"Step {step + 1}: Distance to obstacle = {distance:.2f}, Angle to obstacle = {math.degrees(angle):.2f} degrees")

        # Проверка на столкновение
        if distance < 0.25:  # Порог для столкновения
            print("Collision!")
            break

        # Изменение громкости звука в зависимости от расстояния
        volume = max(0, 1 - (distance / 5))  # Если расстояние больше 5, громкость 0
        wall_sound.set_volume(volume)
        wall_sound.play(maxtime=100)  # Играем звук на короткое время

        # Остановка симуляции, если человек прошел мимо препятствия
        if step > 3 and distance > passing_threshold:
            print("Obstacle passed.")
            break

        # Очистка экрана
        screen.fill(black)

        # Рисование объектов
        pygame.draw.circle(screen, green, (int(person.x * 100 + width // 2), int(-person.y * 100 + height // 2)), 10)  # Позиция человека
        pygame.draw.rect(screen, white, (int(obstacle.x * 100 + width // 2 - 10), int(-obstacle.y * 100 + height // 2 - 50), 20, 100))  # Стена

        # Обновление отображения
        pygame.display.flip()
        pygame.time.delay(100)  # Пауза между шагами симуляции

    pygame.quit()

# Запуск программы
main()
