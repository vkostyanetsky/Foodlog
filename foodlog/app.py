from foodlog.menu import FoodlogMenu
from foodlog.logs_browser import LogsBrowser
from collections import namedtuple
import sys
import yaml



def main_menu() -> None:
    """
    Displays main menu of the application.
    """

    data = __get_data()
    menu = FoodlogMenu(data)

    menu.add_item("Logs Browser", __logs_browser)
    menu.add_item("Statistics", __statistics)
    menu.add_item("Exit", sys.exit)

    menu.choose()


def __logs_browser() -> None:

    data = __get_data()

    LogsBrowser(data).open()

    main_menu()


def __statistics() -> None:

    main_menu()


def __get_data() -> namedtuple:

    data = namedtuple("data", "profile catalog journal weights")

    data.profile = __get_yaml_file_data("profile.yaml")
    data.catalog = __get_yaml_file_data("catalog.yaml")
    data.journal = __get_yaml_file_data("journal.yaml")
    data.weights = __get_yaml_file_data("weights.yaml")

    return data


def __get_yaml_file_data(file_name: str) -> dict:

    try:

        with open(file_name, encoding="utf-8-sig") as yaml_file:
            yaml_file_data = yaml.safe_load(yaml_file)

    except FileNotFoundError:

        print(f"File is not found: {file_name}")
        sys.exit(1)

    return yaml_file_data
