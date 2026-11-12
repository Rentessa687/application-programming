import soundfile as sf

from lab3.audio import print_audio_info, read_audio, write_audio
from lab3.cli import parse_arguments
from lab3.plot import plot_signals
from lab3.transforms import add_echo, add_white_noise, reduce_amplitude


def main() -> None:
    """
    Точка входа: чтение аудио, преобразования, сохранение и графики.
    """
    try:
        args = parse_arguments()
        data, samplerate = read_audio(args.input)
        print_audio_info("Исходное аудио", data, samplerate)

        quieter = reduce_amplitude(data, args.db)
        echoed = add_echo(quieter, samplerate, args.delay, args.decay)
        noisy = add_white_noise(echoed, args.noise)

        print_audio_info("Результат", noisy, samplerate)
        write_audio(args.output, noisy, samplerate)
        print(f"Результат сохранён: {args.output}")

        plot_signals(
            [
                ("Исходное аудио", data),
                (f"Амплитуда уменьшена на {args.db} дБ", quieter),
                (f"Эхо: задержка {args.delay} с, громкость {args.decay}",
                 echoed),
                (f"Белый шум: уровень {args.noise}", noisy),
            ],
            samplerate,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
    except sf.SoundFileError as exc:
        print(f"Audio error: {exc}")
    except OSError as exc:
        print(f"File error: {exc}")


if __name__ == "__main__":
    main()
