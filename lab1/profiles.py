import re


def read_file(path: str) -> str:
    """
    Чтение данных из файла
    :param path: путь до файла
    :return: строковое представление данных из файла
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def split_profiles(text: str) -> list[str]:
    """
    Разделение текста на отдельные анкеты
    :param text: строковое представление данных из файла
    :return: список анкет
    """
    cleaned = text.rstrip()
    return cleaned.split("\n\n")


def extract_name(profile: str) -> str | None:
    """
    Извлечение имени из профиля
    :param profile: профиль человека
    :return: имя человека или None, если в профиле оно не указано
    """
    pattern = r"Имя: (\w+)"
    match = re.search(pattern, profile)
    if match:
        return match.group(1)
    return None
