import csv
import os


class AudioPathIterator:
    """
    Итератор по путям к аудиофайлам.
    Принимает csv-файл аннотации или путь к папке.
    """

    def __init__(self, source: str) -> None:
        """
        :param source: файл аннотации или папка со звуками
        """
        self.paths = self.__load_paths(source)
        self.index = 0

    @staticmethod
    def __load_paths(source: str) -> list[str]:
        """
        Чтение списка путей из аннотации или папки.
        :param source: файл аннотации или папка
        :return: список абсолютных путей
        """
        if os.path.isdir(source):
            names = sorted(os.listdir(source))
            return [
                os.path.abspath(os.path.join(source, name))
                for name in names
                if os.path.isfile(os.path.join(source, name))
            ]
        if os.path.isfile(source):
            with open(source, "r", newline="", encoding="utf-8") as file:
                return [row["absolute_path"] for row in csv.DictReader(file)]
        raise FileNotFoundError(f"Source not found: {source}")

    def __iter__(self) -> "AudioPathIterator":
        """
        :return: сам итератор
        """
        return self

    def __next__(self) -> str:
        """
        :return: следующий путь к файлу
        """
        if self.index >= len(self.paths):
            raise StopIteration
        path = self.paths[self.index]
        self.index += 1
        return path
