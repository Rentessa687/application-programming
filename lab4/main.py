import matplotlib.pyplot as plt
import soundfile as sf

from lab4.cli import parse_arguments
from lab4.dataframe import (
    RELATIVE_PATH,
    SAMPLES_COUNT,
    add_samples_column,
    create_dataframe,
    filter_by_samples,
    name_columns,
    save_dataframe,
    sort_by_samples,
)
from lab4.plot import create_plot, save_plot


def main() -> None:
    """
    Точка входа: DataFrame по аннотации, новая колонка,
    сортировка, фильтрация, график и сохранение.
    """
    try:
        args = parse_arguments()
        df = name_columns(create_dataframe(args.annotation))
        print(f"DataFrame из аннотации ({len(df)} строк):")
        print(df.head())

        df = add_samples_column(df)
        sorted_df = sort_by_samples(df, args.descending)
        print("\nОтсортировано по количеству сэмплов:")
        print(sorted_df[[RELATIVE_PATH, SAMPLES_COUNT]])

        filtered_df = filter_by_samples(sorted_df, args.min, args.max)
        upper = args.max if args.max is not None else "inf"
        print(f"\nФильтр [{args.min}; {upper}], найдено {len(filtered_df)}:")
        print(filtered_df[[RELATIVE_PATH, SAMPLES_COUNT]])

        save_dataframe(sorted_df, args.output_csv)
        print(f"\nDataFrame сохранён: {args.output_csv}")
        fig = create_plot(sorted_df)
        save_plot(fig, args.output_plot)
        print(f"График сохранён: {args.output_plot}")
        plt.show()
    except ValueError as exc:
        print(f"Error: {exc}")
    except sf.SoundFileError as exc:
        print(f"Audio error: {exc}")
    except OSError as exc:
        print(f"File error: {exc}")


if __name__ == "__main__":
    main()
