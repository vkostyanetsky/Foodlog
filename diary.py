import datetime
import os

import yaml
import yaml.parser
from consolemenu import ConsoleMenu, PromptUtils, Screen
from consolemenu.items import FunctionItem


class CaloriesLimitCalculator:
    __profile: dict
    __weights: dict

    def __init__(self, profile: dict, weights: dict) -> None:
        self.__profile = profile
        self.__weights = weights

    def get_calories_limit(self) -> int:

        if self.__profile["calories_limit"] > 0:
            result = self.__profile["calories_limit"]
        else:
            result = self.__get_calculated_daily_calories_limit()

        return result

    def __get_calculated_daily_calories_limit(self) -> int:

        basal_metabolic_rate = self.__get_basal_metabolic_rate()

        calories = basal_metabolic_rate * self.__profile["activity_multiplier"]
        shortage = calories * self.__profile["caloric_deficit"] / 100

        return round(calories - shortage)

    def __get_body_weight(self) -> float:

        if len(self.__weights) > 0:
            body_weight = sorted(self.__weights.items(), key=lambda x: x[0])[-1][1]
        else:
            body_weight = 0

        return float(body_weight)

    def __get_age(self) -> int:

        days_in_year = 365.2425
        days_in_life = (datetime.date.today() - self.__profile["birth_date"]).days

        return int(days_in_life / days_in_year)

    def __get_basal_metabolic_rate(self) -> int:

        weight = self.__get_body_weight()
        height = self.__profile["height"]

        age = self.__get_age()
        bmr = (
            (10 * weight) + (6.25 * height) - (5 * age)
        )  # https://en.wikipedia.org/wiki/Harris–Benedict_equation

        if self.__profile["sex"] == "man":
            bmr += 5
        else:
            bmr -= 161

        return bmr


class FoodEnergyCalculator:
    __journal: list
    __catalog: dict
    __foods: list

    def __init__(self, journal: list, catalog: dict) -> None:
        self.__journal = journal
        self.__catalog = catalog
        self.__foods = []

    def get_food_energy(self) -> tuple:

        total = self.__get_total_template()

        aggregates = self.__get_aggregates_of_journal_for_date()

        for aggregate in aggregates:

            title = aggregate
            grams = aggregates[aggregate]

            food = self.__get_food(title)

            if food is None:
                self.__foods.append(self.__get_food_template(title))
                food = self.__foods[-1]

            attribute_values = self.__catalog[title]

            for attribute in ("calories", "protein", "fat", "carbs"):
                value = round(grams * attribute_values[attribute] / 100)

                food["total"][attribute] += value

                total[attribute] += value

        self.__foods = sorted(
            self.__foods, key=lambda x: x["total"]["calories"], reverse=True
        )

        return self.__foods, total

    def __get_food(self, food_title: str) -> dict:

        foods_list = list(filter(lambda x: x["title"] == food_title, self.__foods))

        return foods_list[0] if len(foods_list) > 0 else None

    def __get_food_template(self, food_title: str) -> dict:

        return {"title": food_title, "total": self.__get_total_template()}

    def __get_food_title_from_catalog(self, food_title: str) -> dict:

        result = None

        for catalog_item in self.__catalog:

            if catalog_item.lower() == food_title.lower():

                if isinstance(self.__catalog[catalog_item], str):
                    result = self.__get_food_title_from_catalog(
                        self.__catalog[catalog_item]
                    )
                else:
                    result = catalog_item
                break

        return result

    def __get_aggregates_of_journal_for_date(self) -> dict:

        result = {}

        for entry in self.__journal:

            is_comment = isinstance(entry, str)

            if is_comment:
                continue

            entry_title = tuple(entry)[0]

            entry_title_from_catalog = self.__get_food_title_from_catalog(entry_title)

            if entry_title_from_catalog is not None:

                entry_grams = tuple(entry.values())[0]

                if result.get(entry_title_from_catalog) is None:
                    result[entry_title_from_catalog] = entry_grams
                else:
                    result[entry_title_from_catalog] += entry_grams

            else:

                print(f'Catalog\'s entry "{entry_title}" is not found.')

        return result

    @staticmethod
    def __get_total_template() -> dict:

        return {
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0,
        }


def run(date_string: str):
    def get_food_offset() -> int:

        result = 0

        for catalog_item in catalog:

            length = len(catalog_item)

            if length > result:
                result = length

        return result + data_offset

    def print_table_row(
        food_value: str,
        calories_value: str,
        protein_value: str,
        fat_value: str,
        carbs_value: str,
    ):

        food_value = food_value.ljust(food_offset)
        calories_value = str(calories_value).ljust(data_offset)
        protein_value = str(protein_value).ljust(data_offset)
        fat_value = str(fat_value).ljust(data_offset)
        carbohydrates_value = str(carbs_value).ljust(data_offset)

        print(food_value, calories_value, protein_value, fat_value, carbohydrates_value)

    def print_nutrients_balance():
        def percent(value: int) -> str:

            if nutrients_total > 0:
                result = round(value * 100 / nutrients_total)
            else:
                result = 0

            result = str(result) + "%"

            return result

        def default_percent(value: str) -> str:

            return f"{value}%"

        nutrients_total = total["protein"] + total["fat"] + total["carbs"]

        protein_percent = percent(total["protein"])
        fat_percent = percent(total["fat"])
        carbs_percent = percent(total["carbs"])

        default_protein_percent = default_percent(profile["protein_percent"])
        default_fat_percent = default_percent(profile["fat_percent"])
        default_carbs_percent = default_percent(profile["carbs_percent"])

        print_table_row(
            "Balance today", "", protein_percent, fat_percent, carbs_percent
        )
        print_table_row(
            "Target ranges",
            "",
            default_protein_percent,
            default_fat_percent,
            default_carbs_percent,
        )

    def print_calories_balance():

        calories_limit = CaloriesLimitCalculator(profile, weights).get_calories_limit()
        calories_to_consume = calories_limit - total["calories"]

        if calories_to_consume >= 0:
            balance_message = f"balance is {calories_to_consume}."
        else:
            balance_message = f"excess is {calories_to_consume * -1}!"

        message = f"Daily calorie intake is {calories_limit} kcal; {balance_message}"

        print(message)

    def print_weight_dynamic():
        def get_yesterday_weight():
            weight_date = get_yesterday_date(date)

            return weights.get(weight_date)

        def get_today_weight():
            weight_date = date

            return weights.get(weight_date)

        def get_tomorrow_weight():
            weight_date = get_tomorrow_date(date)

            return weights.get(weight_date)

        yesterday_weight = get_yesterday_weight()
        today_weight = get_today_weight()
        tomorrow_weight = get_tomorrow_weight()

        if yesterday_weight or today_weight or tomorrow_weight:

            print("Body weight dynamic:")

            if yesterday_weight:
                print(f"- yesterday    {yesterday_weight}")

            if today_weight:
                print(f"- today        {today_weight}")

            if tomorrow_weight:
                print(f"- tomorrow     {tomorrow_weight}")

    def get_yaml_file_data(arg: str) -> dict:

        yaml_filepath = os.path.join(current_directory, f"{arg}.yaml")

        result = {}

        try:

            with open(yaml_filepath, encoding="utf-8-sig") as yaml_file:
                result = yaml.safe_load(yaml_file)

        except FileNotFoundError:

            print(f"File is not found: {yaml_filepath}")

        except yaml.parser.ParserError:

            print(f"Unable to parse {arg}!")

        return result

    current_directory = os.path.abspath(os.path.dirname(__file__))

    profile = get_yaml_file_data("profile")
    journal = get_yaml_file_data("journal")
    weights = get_yaml_file_data("weights")
    catalog = get_yaml_file_data("catalog")

    try:
        date = datetime.datetime.strptime(date_string, get_date_format()).date()
    except ValueError:
        print(f'Unable to convert "{date_string}" to a date.')
        print()
        return

    journal_for_date = journal.get(date)

    if journal_for_date is not None:

        foods, total = FoodEnergyCalculator(journal_for_date, catalog).get_food_energy()

        data_offset = 15
        food_offset = get_food_offset()

        print()

        print_table_row("FOOD", "CALORIES", "PROTEIN", "FAT", "CARBS")
        print()

        for entry in foods:
            print_table_row(
                entry["title"],
                entry["total"]["calories"],
                entry["total"]["protein"],
                entry["total"]["fat"],
                entry["total"]["carbs"],
            )

        print()
        print_table_row(
            "TOTAL", total["calories"], total["protein"], total["fat"], total["carbs"]
        )

        print()
        print_nutrients_balance()

        print()
        print_calories_balance()

        print()
        print_weight_dynamic()

    else:

        print(f"There are no records for {date_string}!")

    print()


def get_date_format():
    return "%Y-%m-%d"


def display_statistics_for_today(prompt_utils):
    date_format = get_date_format()
    date = datetime.date.today().strftime(date_format)

    run(date)
    prompt_utils.enter_to_continue()


def display_statistics_for_date(prompt_utils):
    date_format = get_date_format()
    default_date = get_yesterday_date().strftime(date_format)

    result = prompt_utils.input("Enter a date: ", default=default_date)

    if result.input_string:
        date = result.input_string
    else:
        date = default_date

    run(date)
    prompt_utils.enter_to_continue()


def display_menu():
    """
    Builds and then displays main menu of the application.
    """

    prompt_utils = PromptUtils(Screen())

    menu = ConsoleMenu(
        "FOOD DIARY",
        "Motivation is what gets you started. "
        "Habit is what keeps you going.\n— Jim Ryun",
    )

    menu_item_1 = FunctionItem(
        "Display today's statistics", display_statistics_for_today, [prompt_utils]
    )
    menu_item_2 = FunctionItem(
        "Display statistics for a date", display_statistics_for_date, [prompt_utils]
    )

    menu.append_item(menu_item_1)
    menu.append_item(menu_item_2)

    menu.show()


def get_yesterday_date(date: datetime.date = datetime.date.today()):
    """
    Calculates a date of yesterday for the given date.
    """

    return date - datetime.timedelta(days=1)


def get_tomorrow_date(date: datetime.date = datetime.date.today()):
    """
    Calculates a date of tomorrow for the given date.
    """

    return date + datetime.timedelta(days=1)


if __name__ == "__main__":
    display_menu()
