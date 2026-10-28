from lab1.cli import parse_arguments
from lab1.profiles import (
    read_file, split_profiles, find_by_name, save_profiles
)


def main() -> None:
    """
    Точка входа: поиск анкет по имени и сохранение результата
    """
    try:
        args = parse_arguments()
        text = read_file(args.path)
        profiles = split_profiles(text)
        result = find_by_name(profiles, args.name)
        if not result:
            print("Анкет с таким именем не найдено")
        else:
            save_profiles(result, f"lab1/result_{args.name}.txt")
            print(f"Найдено анкет: {len(result)}")
    except FileNotFoundError as exc:
        print(f"Файл не найден: {exc}")


if __name__ == "__main__":
    main()
