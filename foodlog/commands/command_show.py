from collections import namedtuple
import yaml


def main(path: str, what: str) -> None:
    pass


def __get_data() -> namedtuple:
    """
    Returns app data collection.
    """

    data = namedtuple("data", "profile catalog journal weights")

    data.profile = __get_yaml_file_data("profile.yaml")
    data.catalog = __get_yaml_file_data("catalog.yaml")
    data.journal = __get_yaml_file_data("journal.yaml")
    data.weights = __get_yaml_file_data("weights.yaml")

    return data


def __get_yaml_file_data(file_name: str) -> dict:
    """
    Returns YAML file content as a dictionary.
    """

    try:
        with open(file_name, encoding="utf-8-sig") as yaml_file:
            yaml_file_data = yaml.safe_load(yaml_file)

    except FileNotFoundError:
        print(f"File is not found: {file_name}")
        sys.exit(1)

    return yaml_file_data