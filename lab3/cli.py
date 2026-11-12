import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Разбор аргументов командной строки.
    :return: объект с полученными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Уменьшение амплитуды, эхо и белый шум для аудиофайла"
    )
    parser.add_argument("input", type=str, help="path to source audio file")
    parser.add_argument("output", type=str, help="path to save result")
    parser.add_argument(
        "--db", type=float, default=6.0,
        help="amplitude reduction in decibels (default: 6.0)"
    )
    parser.add_argument(
        "--delay", type=float, default=0.3,
        help="echo delay in seconds (default: 0.3)"
    )
    parser.add_argument(
        "--decay", type=float, default=0.5,
        help="echo volume from 0 to 1 (default: 0.5)"
    )
    parser.add_argument(
        "--noise", type=float, default=0.01,
        help="white noise level (default: 0.01)"
    )
    return parser.parse_args()
