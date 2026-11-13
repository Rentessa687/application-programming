import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Разбор аргументов командной строки.
    :return: объект с полученными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Анализ количества сэмплов в аудиофайлах из аннотации"
    )
    parser.add_argument("annotation", type=str, help="path to annotation csv")
    parser.add_argument("output_csv", type=str, help="path to save dataframe")
    parser.add_argument("output_plot", type=str, help="path to save plot")
    parser.add_argument(
        "--min", type=int, default=0,
        help="minimum number of samples for filter (default: 0)"
    )
    parser.add_argument(
        "--max", type=int, default=None,
        help="maximum number of samples for filter (default: no limit)"
    )
    parser.add_argument(
        "--descending", action="store_true",
        help="sort in descending order"
    )
    return parser.parse_args()
