from food_diary import main

from argparse import ArgumentParser


def get_data_path() -> str:
    parser = ArgumentParser()
    parser.add_argument("path")

    return parser.parse_args().path


if __name__ == "__main__":
    data_path = get_data_path()

    main(data_path)
