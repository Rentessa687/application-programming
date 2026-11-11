import csv
import os

COLUMNS = ["absolute_path", "relative_path"]


def write_annotation(paths: list[str], annotation_path: str) -> None:
    """
    Запись csv-аннотации с абсолютными и относительными путями.
    :param paths: абсолютные пути к файлам
    :param annotation_path: путь к файлу аннотации
    """
    with open(annotation_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(COLUMNS)
        for path in paths:
            writer.writerow([path, os.path.relpath(path)])
