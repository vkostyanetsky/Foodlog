import datetime
from collections import namedtuple

from .food_energy import get_food_energy
from .reference_daily_intake import get_calories_limit


def print_daily_statistics(date_string: str, data: namedtuple) -> None:
    try:
        date = datetime.datetime.strptime(
            date_string, data.profile["date_format"]
        ).date()
    except ValueError:
        print(f'Unable to convert "{date_string}" to a date.')
        print()
        return

    journal_for_date = data.journal[date] if data.journal.get(date) else []

    foods, total = get_food_energy(journal_for_date, data.catalog)

    data_offset = 15
    food_offset = __get_food_offset(data.catalog, data_offset)

    print()

    __print_table_row(
        "FOOD", "CALORIES", "PROTEIN", "FAT", "CARBS", "GRAMS", food_offset, data_offset
    )
    print()

    for entry in foods:
        __print_table_row(
            entry["title"],
            entry["total"]["calories"],
            entry["total"]["protein"],
            entry["total"]["fat"],
            entry["total"]["carbs"],
            entry["total"]["grams"],
            food_offset,
            data_offset,
        )

    print()
    __print_table_row(
        "TOTAL",
        total["calories"],
        total["protein"],
        total["fat"],
        total["carbs"],
        "",
        food_offset,
        data_offset,
    )

    print()
    __print_nutrients_balance(data, total, food_offset, data_offset)

    print()
    __print_calories_balance(data, total)

    print()
    __print_weight_dynamic(date, data)

    print()


def __get_food_offset(catalog: dict, data_offset: int) -> int:
    result = 0

    for catalog_item in catalog:

        length = len(catalog_item)

        if length > result:
            result = length

    return result + data_offset


def __print_table_row(
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

    print(
        food_value,
        calories_value,
        protein_value,
        fat_value,
        carbohydrates_value,
        grams_value,
    )


def __percent(nutrients_total: int, value: int) -> str:
    if nutrients_total > 0:
        result = round(value * 100 / nutrients_total)
    else:
        result = 0

    result = str(result) + "%"

    return result


def __print_nutrients_balance(
    data: namedtuple, total: dict, food_offset: int, data_offset: int
):

    nutrients_total = total["protein"] + total["fat"] + total["carbs"]

    protein_percent = __percent(nutrients_total, total["protein"])
    fat_percent = __percent(nutrients_total, total["fat"])
    carbs_percent = __percent(nutrients_total, total["carbs"])

    default_protein_percent = f"{data.profile['protein_percent']}%"
    default_fat_percent = f"{data.profile['fat_percent']}%"
    default_carbs_percent = f"{data.profile['carbs_percent']}%"

    __print_table_row(
        "Balance today",
        "",
        protein_percent,
        fat_percent,
        carbs_percent,
        "",
        food_offset,
        data_offset,
    )

    __print_table_row(
        "Target ranges",
        "",
        default_protein_percent,
        default_fat_percent,
        default_carbs_percent,
        "",
        food_offset,
        data_offset,
    )


def __print_calories_balance(data: namedtuple, total: dict):
    calories_limit = get_calories_limit(data.profile, data.weights)
    calories_to_consume = calories_limit - total["calories"]

    if calories_to_consume >= 0:
        balance_message = f"balance is {calories_to_consume}."
    else:
        balance_message = f"excess is {calories_to_consume * -1}!"

    message = f"Daily calorie intake is {calories_limit} kcal; {balance_message}"

    print(message)


def __print_weight_dynamic(date: datetime.date, data: namedtuple):
    yesterday_weight = data.weights.get(date - datetime.timedelta(days=1))
    today_weight = data.weights.get(date)
    tomorrow_weight = data.weights.get(date + datetime.timedelta(days=1))

    if yesterday_weight or today_weight or tomorrow_weight:

        print("Body weight dynamic:")

        if yesterday_weight:
            print(f"- yesterday    {yesterday_weight}")

        if today_weight:
            print(f"- today        {today_weight}")

        if tomorrow_weight:
            print(f"- tomorrow     {tomorrow_weight}")
