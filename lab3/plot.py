import matplotlib.pyplot as plt
import numpy as np


def plot_signals(
    signals: list[tuple[str, np.ndarray]], samplerate: int
) -> None:
    """
    Построение графиков амплитуды для нескольких аудиосигналов.
    :param signals: список пар (заголовок, массив сэмплов)
    :param samplerate: частота дискретизации
    """
    fig, axes = plt.subplots(
        len(signals), 1, figsize=(12, 3 * len(signals)),
        sharex=True, sharey=True
    )
    for ax, (title, data) in zip(axes, signals):
        time = np.arange(data.shape[0]) / samplerate
        ax.plot(time, data, linewidth=0.5)
        ax.set_title(title)
        ax.set_ylabel("Амплитуда")
        ax.set_ylim(-1.0, 1.0)
        ax.grid(color="gray", linestyle="--", linewidth=0.5)
    axes[-1].set_xlabel("Время, с")
    fig.tight_layout()
    plt.show()
