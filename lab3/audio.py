import os

import numpy as np
import soundfile as sf


def read_audio(path: str) -> tuple[np.ndarray, int]:
    """
    Чтение аудиофайла.
    :param path: путь к файлу
    :return: массив сэмплов и частота дискретизации
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    data, samplerate = sf.read(path)
    return data, samplerate


def write_audio(path: str, data: np.ndarray, samplerate: int) -> None:
    """
    Сохранение аудио в файл.
    :param path: путь для сохранения
    :param data: массив сэмплов
    :param samplerate: частота дискретизации
    """
    extension = os.path.splitext(path)[1].lstrip(".").upper()
    if extension not in sf.available_formats():
        raise ValueError(f"Unsupported audio format: {path}")
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    sf.write(path, data, samplerate)


def print_audio_info(title: str, data: np.ndarray, samplerate: int) -> None:
    """
    Вывод размера и параметров аудио.
    :param title: заголовок
    :param data: массив сэмплов
    :param samplerate: частота дискретизации
    """
    channels = 1 if data.ndim == 1 else data.shape[1]
    print(f"{title}:")
    print(f"  размер массива: {data.shape}")
    print(f"  количество сэмплов: {data.shape[0]}")
    print(f"  количество каналов: {channels}")
    print(f"  частота дискретизации: {samplerate} Hz")
    print(f"  длительность: {data.shape[0] / samplerate:.2f} s")
