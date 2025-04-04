import os
import librosa
import soundfile as sf
import numpy as np

def enhance_volume(input_file, output_file, target_dB=-15, boost_gain=1.5):
    try:
        # Загрузка аудио с сохранением оригинальной частоты дискретизации
        audio, sample_rate = librosa.load(input_file, sr=None)
        
        # Вычисление текущего RMS уровня
        current_rms = np.sqrt(np.mean(audio**2))
        
        # Расчет коэффициента усиления
        current_db = 20 * np.log10(current_rms)
        gain = 10 ** ((target_dB - current_db) / 20) * boost_gain
        
        # Применение усиления с дополнительным усилением
        enhanced_audio = audio * gain
        
        # Мягкое ограничение амплитуды, чтобы избежать сильных искажений
        enhanced_audio = np.clip(enhanced_audio, -1, 1)
        
        # Сохранение усиленного аудио
        sf.write(output_file, enhanced_audio, sample_rate)
        
        print(f"Файл {input_file} успешно усилен!")
    except Exception as e:
        print(f"Ошибка при обработке файла {input_file}: {e}")

def enhance_volume_files():
    # Список файлов для усиления
    files_to_process = [
        'wall.wav',
        'column.wav'
    ]
    
    # Создаем папку для обработанных файлов, если её нет
    output_dir = 'enhanced_audio'
    os.makedirs(output_dir, exist_ok=True)
    
    # Обработка каждого файла
    for input_file in files_to_process:
        # Проверяем существование файла
        if os.path.exists(input_file):
            # Формируем путь для выходного файла
            output_file = os.path.join(output_dir, f'enhanced_{input_file}')
            
            # Усиление аудио
            enhance_volume(input_file, output_file)
        else:
            print(f"Файл {input_file} не найден!")

# Запуск усиления файлов
enhance_volume_files()

