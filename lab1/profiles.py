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


def find_by_name(profiles: list[str], name: str) -> list[str]:
    """
    Поиск анкет по имени без учёта регистра
    :param profiles: список анкет
    :param name: имя, по которому будет выполнен поиск
    :return: анкеты, у которых имя совпало с искомым без учёта регистра
    """
    result = []
    for profile in profiles:
        extracted_name = extract_name(profile)
        if extracted_name is not None:
            if extracted_name.lower() == name.lower():
                result.append(profile)
    return result


def save_profiles(profiles: list[str], path: str) -> None:
    """
    Записывает анкеты в файл в том же формате, что и в исходнике
    :param profiles: список анкет
    :param path: путь к файлу для сохранения
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n\n".join(profiles))
