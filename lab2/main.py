import requests

from lab2.annotation import write_annotation
from lab2.cli import parse_arguments
from lab2.iterator import AudioPathIterator
from lab2.scraper import (
    BASE_URL,
    collect_links,
    download_file,
    fetch_html,
    find_category_url,
    get_categories,
    get_sound_id,
)

MIN_FILES = 30


def download_category(
    category_url: str, count: int, folder: str, seen: set[str]
) -> list[str]:
    """
    Скачивание звуков одной категории.
    :param category_url: адрес категории
    :param count: сколько звуков скачать
    :param folder: папка для сохранения
    :param seen: идентификаторы уже скачанных звуков
    :return: абсолютные пути к скачанным файлам
    """
    paths = []
    links = collect_links(category_url, count * 3)
    for link in links:
        if len(paths) == count:
            break
        sound_id = get_sound_id(link)
        if sound_id in seen:
            continue
        try:
            paths.append(download_file(link, folder))
            seen.add(sound_id)
        except (requests.RequestException, ValueError) as exc:
            print(f"Skipped {link}: {exc}")
    return paths


def main() -> None:
    """
    Точка входа: скачивание звуков, запись аннотации, проверка итератора.
    """
    try:
        args = parse_arguments()
        categories = get_categories(fetch_html(BASE_URL))
        all_paths: list[str] = []
        seen: set[str] = set()
        for name in args.categories:
            url = find_category_url(categories, name)
            paths = download_category(url, args.count, args.folder, seen)
            print(f"{name}: скачано {len(paths)} из {args.count}")
            all_paths.extend(paths)
        write_annotation(all_paths, args.annotation)
        print(f"Всего скачано файлов: {len(all_paths)}")
        if len(all_paths) < MIN_FILES:
            print(f"Внимание: меньше {MIN_FILES} файлов, увеличьте count")
        for path in AudioPathIterator(args.annotation):
            print(path)
    except ValueError as exc:
        print(f"Error: {exc}")
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
    except OSError as exc:
        print(f"File error: {exc}")


if __name__ == "__main__":
    main()
