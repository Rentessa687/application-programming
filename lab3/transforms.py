import numpy as np

MIN_AMPLITUDE = -1.0
MAX_AMPLITUDE = 1.0


def reduce_amplitude(data: np.ndarray, decibels: float) -> np.ndarray:
    """
    Уменьшение амплитуды сэмплов на заданное количество децибел.
    :param data: массив сэмплов
    :param decibels: на сколько децибел уменьшить громкость
    :return: новый массив сэмплов
    """
    if decibels < 0:
        raise ValueError("Decibels must be non-negative")
    factor = 10 ** (-decibels / 20)
    return data * factor


def add_echo(
    data: np.ndarray, samplerate: int, delay: float, decay: float
) -> np.ndarray:
    """
    Эхо-эффект: наложение задержанной и ослабленной копии звука.
    :param data: массив сэмплов
    :param samplerate: частота дискретизации
    :param delay: задержка эха в секундах
    :param decay: громкость эха относительно исходного звука (0..1)
    :return: новый массив сэмплов (длиннее исходного на задержку)
    """
    if delay <= 0:
        raise ValueError("Delay must be positive")
    if not 0 <= decay <= 1:
        raise ValueError("Decay must be between 0 and 1")
    shift = int(delay * samplerate)
    result = np.zeros((data.shape[0] + shift, *data.shape[1:]))
    result[:data.shape[0]] += data
    result[shift:] += data * decay
    return np.clip(result, MIN_AMPLITUDE, MAX_AMPLITUDE)


def add_white_noise(data: np.ndarray, level: float) -> np.ndarray:
    """
    Добавление белого шума.
    :param data: массив сэмплов
    :param level: уровень шума (стандартное отклонение)
    :return: новый массив сэмплов
    """
    if level < 0:
        raise ValueError("Noise level must be non-negative")
    noise = np.random.default_rng().normal(0.0, level, data.shape)
    return np.clip(data + noise, MIN_AMPLITUDE, MAX_AMPLITUDE)
