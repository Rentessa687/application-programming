import os

import pandas as pd

from lab4.audio import get_samples_count

ABSOLUTE_PATH = "absolute_path"
RELATIVE_PATH = "relative_path"
SAMPLES_COUNT = "samples_count"


def create_dataframe(annotation_path: str) -> pd.DataFrame:
    """
    Создание DataFrame из файла аннотации.
    :param annotation_path: путь к csv-файлу аннотации
    :return: DataFrame с двумя колонками путей
    """
    if not os.path.isfile(annotation_path):
        raise FileNotFoundError(f"File not found: {annotation_path}")
    df = pd.read_csv(annotation_path)
    if len(df.columns) != 2:
        raise ValueError("Annotation must contain exactly 2 columns")
    return df


def name_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Именование колонок DataFrame.
    :param df: DataFrame с двумя колонками путей
    :return: DataFrame с колонками absolute_path и relative_path
    """
    df = df.copy()
    df.columns = [ABSOLUTE_PATH, RELATIVE_PATH]
    return df


def add_samples_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с количеством сэмплов каждого аудиофайла.
    :param df: DataFrame с колонкой абсолютных путей
    :return: DataFrame с новой колонкой samples_count
    """
    df = df.copy()
    df[SAMPLES_COUNT] = df[ABSOLUTE_PATH].apply(get_samples_count)
    return df


def sort_by_samples(
    df: pd.DataFrame, descending: bool = False
) -> pd.DataFrame:
    """
    Сортировка по количеству сэмплов.
    :param df: DataFrame с колонкой samples_count
    :param descending: сортировать по убыванию
    :return: отсортированный DataFrame
    """
    return df.sort_values(
        SAMPLES_COUNT, ascending=not descending, ignore_index=True
    )


def filter_by_samples(
    df: pd.DataFrame, min_samples: int, max_samples: int | None = None
) -> pd.DataFrame:
    """
    Фильтрация по количеству сэмплов.
    :param df: DataFrame с колонкой samples_count
    :param min_samples: минимальное количество сэмплов (включительно)
    :param max_samples: максимальное количество сэмплов (включительно)
    :return: DataFrame только с подходящими строками
    """
    if min_samples < 0:
        raise ValueError("Minimum must be non-negative")
    if max_samples is not None and max_samples < min_samples:
        raise ValueError("Maximum must be greater than or equal to minimum")
    mask = df[SAMPLES_COUNT] >= min_samples
    if max_samples is not None:
        mask &= df[SAMPLES_COUNT] <= max_samples
    return df[mask].reset_index(drop=True)


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Сохранение DataFrame в csv-файл.
    :param df: DataFrame
    :param path: путь для сохранения
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    df.to_csv(path, index=False)
