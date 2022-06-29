import datetime
import sys
from argparse import ArgumentParser
from collections import namedtuple
from os.path import join

from consolemenu import ConsoleMenu, PromptUtils, Screen
from consolemenu.items import FunctionItem
from .daily_statistics import print_daily_statistics
from yaml import parser, safe_load


def main() -> None:

    data_path = get_data_path()
    data = namedtuple("data", "profile catalog journal weights")

    data.profile = get_yaml_file_data(data_path, "profile.yaml")
    data.catalog = get_yaml_file_data(data_path, "catalog.yaml")
    data.journal = get_yaml_file_data(data_path, "journal.yaml")
    data.weights = get_yaml_file_data(data_path, "weights.yaml")

    display_menu(data)


def get_data_path() -> str:
    argument_parser = ArgumentParser()
    argument_parser.add_argument("path")

    return argument_parser.parse_args().path


def get_yaml_file_data(data_path: str, file_name: str) -> dict:
    yaml_file_path = join(data_path, file_name)

    try:

        with open(yaml_file_path, encoding="utf-8-sig") as yaml_file:
            yaml_file_data = safe_load(yaml_file)

    except FileNotFoundError:

        print(f"File is not found: {yaml_file_path}")
        sys.exit(1)

    except parser.ParserError:

        print(f"Unable to parse: {yaml_file_path}")
        sys.exit(1)

    return yaml_file_data


def display_menu(data: namedtuple):
    """
    Builds and then displays main menu of the application.
    """

    prompt_utils = PromptUtils(Screen())
    items_params = [data, prompt_utils]

    menu = ConsoleMenu(
        "FOOD DIARY",
        "Motivation is what gets you started. "
        "Habit is what keeps you going.\n— Jim Ryun",
    )

    menu.append_item(
        FunctionItem(
            "Display today's statistics", display_statistics_for_today, items_params
        )
    )

    menu.append_item(
        FunctionItem(
            "Display statistics for a date", display_statistics_for_date, items_params
        )
    )

    menu.show()


def display_statistics_for_today(data: namedtuple, prompt_utils: PromptUtils):
    date = datetime.date.today().strftime(data.profile["date_format"])

    print_daily_statistics(date, data)

    prompt_utils.enter_to_continue()


def display_statistics_for_date(data: namedtuple, prompt_utils: PromptUtils):
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    default_date = yesterday_date.strftime(data.profile["date_format"])

    result = prompt_utils.input("Enter a date: ", default=default_date)

    if result.input_string:
        date = result.input_string
    else:
        date = default_date

    print_daily_statistics(date, data)
    prompt_utils.enter_to_continue()
