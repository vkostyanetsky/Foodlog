import os
import sys
from collections import namedtuple

import yaml

from foodlog import logs_viewer, echo


def main(path: str, what: str) -> None:
    """
    Outputs a detailed view of a day income.
    """

    data = __get_data(path)

    if data:
        if what == "last":
            __show_last(data)
        elif what == "prev":
            __show_prev(data)

    else:
        echo.line("Nothing to show, since there are no logs.")


def __show_last(data) -> None:
    logs_viewer.view(-1, data)


def __show_prev(data) -> None:
    if len(data) >= 2:
        logs_viewer.view(-2, data)

    else:
        echo.line("Nothing to show, since there is no previous day with logs.")


def __get_data(path: str) -> namedtuple:
    """
    Returns app data collection.
    """

    data = namedtuple("data", "profile catalog journal weights")

    data.profile = __get_yaml_file_data(path, "profile.yaml")
    data.catalog = __get_yaml_file_data(path, "catalog.yaml")
    data.journal = __get_yaml_file_data(path, "journal.yaml")
    data.weights = __get_yaml_file_data(path, "weights.yaml")

    return data


def __get_yaml_file_data(path: str, file_name: str) -> dict:
    """
    Returns YAML file content as a dictionary.
    """

    file_path = os.path.join(path, file_name)

    try:
        with open(file_path, encoding="utf-8-sig") as yaml_file:
            yaml_file_data = yaml.safe_load(yaml_file)

    except FileNotFoundError:
        print(f"File is not found: {file_name}")
        sys.exit(1)

    return yaml_file_data
