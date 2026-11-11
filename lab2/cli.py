import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Разбор аргументов командной строки.
    :return: объект с полученными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Скачивание звуков с sound-effects.ru по категориям"
    )
    parser.add_argument("folder", type=str, help="folder for sounds")
    parser.add_argument("annotation", type=str, help="path to csv file")
    parser.add_argument(
        "count", type=int, help="number of sounds per category"
    )
    parser.add_argument(
        "categories", nargs="+", help="one or more category names"
    )
    return parser.parse_args()
