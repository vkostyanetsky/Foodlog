#!/usr/bin/env python3

"""
Main app's menu generator.
"""

import datetime
from collections import namedtuple

from vkostyanetsky.cliutils import Menu, title_and_value

from foodlog import calculator, reference_daily_intake


class FoodlogMenu(Menu):
    """
    Class of the main app's menu.
    """

    _data: namedtuple
    _summary_titles_width: int = 10

    def __init__(self, data: namedtuple):
        super().__init__()

        self._data = data

    def _print_menu(self):
        print(self._top_border())

        self._print_title()

        self._print_summary()

        self._print_choices()

        print(self._bottom_border())

    def _print_title(self):
        print(self._text_line("FOOD LOG", 2))

        print(self._inner_border())

    def _print_choices(self):
        print(self._empty_line())

        for choice in self._get_choices_to_print():
            print(self._text_line(text=choice))

        print(self._empty_line())

    def _get_total_for_today(self):
        date_today = datetime.date.today()
        journal = (
            self._data.journal[date_today]
            if self._data.journal.get(date_today) is not None
            else []
        )

        totals = calculator.totals(journal, self._data.catalog)

        return totals["total"]

    def _get_calories_summary(self, totals_for_today: dict) -> str:
        calories_limit = reference_daily_intake.get_calories_limit(
            self._data.profile, self._data.weights
        )
        calories_today = totals_for_today.get("calories")

        if calories_today < calories_limit:
            calories_suffix = f" ({calories_limit - calories_today} left)"
        elif calories_today > calories_limit:
            calories_suffix = f" ({calories_today - calories_limit} extra)"
        else:
            calories_suffix = ""

        return f"{calories_today} out of {calories_limit}{calories_suffix}"

    def _print_calories_summary(self, totals_for_today: dict) -> None:
        calories = title_and_value(
            title="Calories",
            value=self._get_calories_summary(totals_for_today),
            width=self._summary_titles_width,
        )
        calories = self._text_line(calories)

        print(calories)

    def _print_nutrient_balance(self, balance: dict, key: str, title: str):
        balance_value = balance[key]
        profile_value = self._data.profile[key]

        text = title_and_value(
            title=title,
            value=f"{balance_value}% (aim is {profile_value}%)",
            width=self._summary_titles_width,
        )

        print(self._text_line(text))

    def _print_nutrients_balance(self, totals_for_today: dict) -> None:
        balance = calculator.nutrients_balance(totals_for_today)

        self._print_nutrient_balance(balance, "protein_percent", "Protein")
        self._print_nutrient_balance(balance, "fat_percent", "Fat")
        self._print_nutrient_balance(balance, "carbs_percent", "Carbs")

    def _print_summary(self):
        total_for_today = self._get_total_for_today()

        print(self._empty_line())

        print(self._text_line("SUMMARY FOR TODAY"))
        print(self._empty_line())

        self._print_calories_summary(total_for_today)
        self._print_nutrients_balance(total_for_today)

        print(self._empty_line())
        print(self._inner_border())

    def print(self):
        """
        Draws the menu.
        """
        print()

        self._print_menu()

        print(self._prompt, end="")
