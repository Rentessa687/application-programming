import os

import matplotlib.pyplot as plt
import pandas as pd

from lab4.dataframe import SAMPLES_COUNT


def create_plot(df: pd.DataFrame) -> plt.Figure:
    """
    Построение графиков по количеству сэмплов.
    Слева - значения для каждого файла в отсортированном порядке,
    справа - гистограмма распределения.
    :param df: отсортированный DataFrame с колонкой samples_count
    :return: фигура с графиками
    """
    fig, (ax_bar, ax_hist) = plt.subplots(1, 2, figsize=(14, 5))

    ax_bar.bar(range(1, len(df) + 1), df[SAMPLES_COUNT])
    ax_bar.set_title("Количество сэмплов в каждом файле (отсортировано)")
    ax_bar.set_xlabel("Номер файла в отсортированном списке")
    ax_bar.set_ylabel("Количество сэмплов")

    ax_hist.hist(df[SAMPLES_COUNT], bins=10, edgecolor="black")
    ax_hist.set_title("Распределение количества сэмплов")
    ax_hist.set_xlabel("Количество сэмплов")
    ax_hist.set_ylabel("Количество файлов")

    for ax in (ax_bar, ax_hist):
        ax.grid(color="gray", linestyle="--", linewidth=0.5)
    fig.tight_layout()
    return fig


def save_plot(fig: plt.Figure, path: str) -> None:
    """
    Сохранение графика в файл.
    :param fig: фигура с графиками
    :param path: путь для сохранения
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fig.savefig(path)
