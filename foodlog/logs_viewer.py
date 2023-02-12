#!/usr/bin/env python3

"""
Journal reading functionality.
"""

import datetime
from collections import namedtuple

from foodlog import calculator, reference_daily_intake


def get(log_index: int, data: namedtuple) -> list:
    """
    Returns information from a journal log by an index given.
    """

    journal_date = list(data.journal.keys())[log_index]
    journal_entry = list(data.journal.values())[log_index]

    lines = [journal_date]
    totals = calculator.totals(journal_entry, data.catalog)

    data_offset = 15
    food_offset = __get_food_offset(data.catalog, data_offset)

    lines.append("")

    __add_table_row(
        lines,
        {
            "food": "FOOD",
            "calories": "CALORIES",
            "protein": "PROTEIN",
            "fat": "FAT",
            "carbs": "CARBS",
            "grams": "GRAMS",
        },
        food_offset,
        data_offset,
    )
    lines.append("")

    for entry in totals["foods"]:
        __add_table_row(
            lines,
            {
                "food": entry["title"],
                "calories": entry["total"]["calories"],
                "protein": entry["total"]["protein"],
                "fat": entry["total"]["fat"],
                "carbs": entry["total"]["carbs"],
                "grams": entry["total"]["grams"],
            },
            food_offset,
            data_offset,
        )

    lines.append("")

    __add_table_row(
        lines,
        {
            "food": "TOTAL",
            "calories": totals["total"]["calories"],
            "protein": totals["total"]["protein"],
            "fat": totals["total"]["fat"],
            "carbs": totals["total"]["carbs"],
            "grams": "",
        },
        food_offset,
        data_offset,
    )

    lines.append("")
    __print_nutrients_balance(lines, data, totals["total"], food_offset, data_offset)

    lines.append("")
    __print_calories_balance(lines, data, totals["total"])

    lines.append("")
    __print_weight_dynamic(lines, journal_date, data)

    return lines


def __get_food_offset(catalog: dict, data_offset: int) -> int:
    result = 0

    for catalog_item in catalog:
        length = len(catalog_item)

        if length > result:
            result = length

    return result + data_offset


def __add_table_row(lines: list, columns: dict, food_offset: int, data_offset: int):
    food = columns["food"].ljust(food_offset)
    calories = str(columns["calories"]).ljust(data_offset)
    protein = str(columns["protein"]).ljust(data_offset)
    fat = str(columns["fat"]).ljust(data_offset)
    carbs = str(columns["carbs"]).ljust(data_offset)
    grams = str(columns["grams"]).ljust(data_offset)

    lines.append(f"{food}{calories}{protein}{fat}{carbs}{grams}")


def __percent(nutrients_total: int, value: int) -> str:
    if nutrients_total > 0:
        result = round(value * 100 / nutrients_total)
    else:
        result = 0

    result = str(result) + "%"

    return result


def __print_nutrients_balance(
    result: list, data: namedtuple, total: dict, food_offset: int, data_offset: int
):
    nutrients_total = total["protein"] + total["fat"] + total["carbs"]

    protein_percent = __percent(nutrients_total, total["protein"])
    fat_percent = __percent(nutrients_total, total["fat"])
    carbs_percent = __percent(nutrients_total, total["carbs"])

    default_protein_percent = f"{data.profile['protein_percent']}%"
    default_fat_percent = f"{data.profile['fat_percent']}%"
    default_carbs_percent = f"{data.profile['carbs_percent']}%"

    __add_table_row(
        result,
        {
            "food": "Balance today",
            "calories": "",
            "protein": protein_percent,
            "fat": fat_percent,
            "carbs": carbs_percent,
            "grams": "",
        },
        food_offset,
        data_offset,
    )

    __add_table_row(
        result,
        {
            "food": "Target ranges",
            "calories": "",
            "protein": default_protein_percent,
            "fat": default_fat_percent,
            "carbs": default_carbs_percent,
            "grams": "",
        },
        food_offset,
        data_offset,
    )


def __print_calories_balance(lines: list, data: namedtuple, total: dict):
    calories_limit = reference_daily_intake.get_calories_limit(
        data.profile, data.weights
    )
    calories_to_consume = calories_limit - total["calories"]

    if calories_to_consume >= 0:
        balance_message = f"balance is {calories_to_consume}."
    else:
        balance_message = f"excess is {calories_to_consume * -1}!"

    message = f"Daily calorie intake is {calories_limit} kcal; {balance_message}"

    lines.append(message)


def __print_weight_dynamic(lines: list, date: datetime.date, data: namedtuple):
    yesterday_weight = data.weights.get(date - datetime.timedelta(days=1))
    today_weight = data.weights.get(date)
    tomorrow_weight = data.weights.get(date + datetime.timedelta(days=1))

    if yesterday_weight or today_weight or tomorrow_weight:
        lines.append("Body weight dynamic:")

        if yesterday_weight:
            lines.append(f"- yesterday    {yesterday_weight}")

        if today_weight:
            lines.append(f"- today        {today_weight}")

        if tomorrow_weight:
            lines.append(f"- tomorrow     {tomorrow_weight}")
