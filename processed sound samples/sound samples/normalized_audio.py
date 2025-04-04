import os
import librosa
import soundfile as sf
import numpy as np

def normalize_audio(input_file, output_file, target_dB=-20):
    try:
        # Загрузка аудио с сохранением оригинальной частоты дискретизации
        audio, sample_rate = librosa.load(input_file, sr=None)
        
        # Вычисление текущего RMS уровня
        current_rms = np.sqrt(np.mean(audio**2))
        
        # Расчет коэффициента усиления
        # Используем логарифмическую шкалу для более точной нормализации
        current_db = 20 * np.log10(current_rms)
        gain = 10 ** ((target_dB - current_db) / 20)
        
        # Применение усиления
        normalized_audio = audio * gain
        
        # Мягкое ограничение амплитуды, чтобы избежать клиппинга
        normalized_audio = np.clip(normalized_audio, -1, 1)
        
        # Сохранение нормализованного аудио
        sf.write(output_file, normalized_audio, sample_rate)
        
        print(f"Файл {input_file} успешно нормализован!")
    except Exception as e:
        print(f"Ошибка при обработке файла {input_file}: {e}")

def normalize_all_audio_files():
    # Список файлов для обработки
    files_to_process = [
        # Первая группа
        'entranceexit.wav',
        'turnstile.wav', 
        'administration_desk.wav',
        
        # Вторая группа
        'furniture.wav',
        'approach_to the_doorway.wav', 
        'wardrobe.wav',
        'vending_machine_with drinks.wav',
        
        # Третья группа
        'ATM_machine.wav',
        
        # Четвертая группа
        'dining_room.wav',
        'ladder.wav',
        'student_office.wav',
        
        # Новые файлы
        'wall.wav',
        'column.wav'
    ]
    
    # Создаем папку для нормализованных файлов, если её нет
    output_dir = 'normalized_audio'
    os.makedirs(output_dir, exist_ok=True)
    
    # Обработка каждого файла
    for input_file in files_to_process:
        # Проверяем существование файла
        if os.path.exists(input_file):
            # Формируем путь для выходного файла
            output_file = os.path.join(output_dir, f'normalized_{input_file}')
            
            # Нормализация аудио
            normalize_audio(input_file, output_file)
        else:
            print(f"Файл {input_file} не найден!")

# Запуск нормализации всех файлов
normalize_all_audio_files()
