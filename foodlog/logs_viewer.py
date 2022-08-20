import datetime
from collections import namedtuple
from foodlog import calculator
from foodlog import reference_daily_intake


def get(log_index: int, data: namedtuple) -> list:

    journal_date = list(data.journal.keys())[log_index]
    journal_entry = list(data.journal.values())[log_index]

    result = [journal_date]
    totals = calculator.totals(journal_entry, data.catalog)  # foods, total

    data_offset = 15
    food_offset = __get_food_offset(data.catalog, data_offset)

    result.append("")

    __add_table_row(
        result, "FOOD", "CALORIES", "PROTEIN", "FAT", "CARBS", "GRAMS", food_offset, data_offset
    )
    result.append("")

    for entry in totals["foods"]:
        __add_table_row(
            result,
            entry["title"],
            entry["total"]["calories"],
            entry["total"]["protein"],
            entry["total"]["fat"],
            entry["total"]["carbs"],
            entry["total"]["grams"],
            food_offset,
            data_offset,
        )

    result.append("")

    __add_table_row(
        result,
        "TOTAL",
        totals["total"]["calories"],
        totals["total"]["protein"],
        totals["total"]["fat"],
        totals["total"]["carbs"],
        "",
        food_offset,
        data_offset,
    )

    result.append("")
    __print_nutrients_balance(result, data, totals["total"], food_offset, data_offset)

    result.append("")
    __print_calories_balance(result, data, totals["total"])

    result.append("")
    __print_weight_dynamic(result, journal_date, data)

    result.append("")

    return result


def __get_food_offset(catalog: dict, data_offset: int) -> int:
    result = 0

    for catalog_item in catalog:

        length = len(catalog_item)

        if length > result:
            result = length

    return result + data_offset


def __add_table_row(
    result,
    food_value: str,
    calories_value: str,
    protein_value: str,
    fat_value: str,
    carbs_value: str,
    grams_value: str,
    food_offset: int,
    data_offset: int,
):
    food_value = food_value.ljust(food_offset)
    calories_value = str(calories_value).ljust(data_offset)
    protein_value = str(protein_value).ljust(data_offset)
    fat_value = str(fat_value).ljust(data_offset)
    carbohydrates_value = str(carbs_value).ljust(data_offset)
    grams_value = str(grams_value).ljust(data_offset)

    result.append(f"{food_value}{calories_value}{protein_value}{fat_value}{carbohydrates_value}{grams_value}")


def __percent(nutrients_total: int, value: int) -> str:
    if nutrients_total > 0:
        result = round(value * 100 / nutrients_total)
    else:
        result = 0

    result = str(result) + "%"

    return result


def __print_nutrients_balance(
    result, data: namedtuple, total: dict, food_offset: int, data_offset: int
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
        "Balance today",
        "",
        protein_percent,
        fat_percent,
        carbs_percent,
        "",
        food_offset,
        data_offset,
    )

    __add_table_row(
        result,
        "Target ranges",
        "",
        default_protein_percent,
        default_fat_percent,
        default_carbs_percent,
        "",
        food_offset,
        data_offset,
    )


def __print_calories_balance(result, data: namedtuple, total: dict):
    calories_limit = reference_daily_intake.get_calories_limit(data.profile, data.weights)
    calories_to_consume = calories_limit - total["calories"]

    if calories_to_consume >= 0:
        balance_message = f"balance is {calories_to_consume}."
    else:
        balance_message = f"excess is {calories_to_consume * -1}!"

    message = f"Daily calorie intake is {calories_limit} kcal; {balance_message}"

    result.append(message)


def __print_weight_dynamic(result, date: datetime.date, data: namedtuple):
    yesterday_weight = data.weights.get(date - datetime.timedelta(days=1))
    today_weight = data.weights.get(date)
    tomorrow_weight = data.weights.get(date + datetime.timedelta(days=1))

    if yesterday_weight or today_weight or tomorrow_weight:

        result.append("Body weight dynamic:")

        if yesterday_weight:
            result.append(f"- yesterday    {yesterday_weight}")

        if today_weight:
            result.append(f"- today        {today_weight}")

        if tomorrow_weight:
            result.append(f"- tomorrow     {tomorrow_weight}")
