import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Разбор аргументов командной строки.
    :return: объект с полученными аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path to the file with profiles")
    parser.add_argument("name", type=str, help="name for search")
    return parser.parse_args()
