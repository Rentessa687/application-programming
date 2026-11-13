import os

import soundfile as sf


def get_samples_count(path: str) -> int:
    """
    Подсчёт количества сэмплов в аудиофайле.
    Если файл повреждён и не читается до конца,
    количество берётся из заголовка файла.
    :param path: путь к аудиофайлу
    :return: количество сэмплов
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        data, _ = sf.read(path)
        return data.shape[0]
    except sf.LibsndfileError:
        return sf.info(path).frames
