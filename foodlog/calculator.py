#!/usr/bin/env python3

"""
Totals calculating functionality.
"""

import re


def totals(journal: list, catalog: dict) -> dict:
    """
    Returns totals for a journal.
    """

    foods = []
    total = __get_total_template()

    aggregates = __get_aggregates_of_journal_for_date(journal, catalog)

    for title, grams in aggregates.items():
        food = __get_food(foods, title)

        if food is None:
            foods.append(__get_food_template(title))
            food = foods[-1]

        attribute_values = catalog[title]

        for attribute in ("calories", "protein", "fat", "carbs", "grams"):
            if attribute == "grams":
                value = grams
            else:
                value = round(grams * attribute_values[attribute] / 100)

            food["total"][attribute] += value

            total[attribute] += value

    foods = sorted(foods, key=lambda x: x["total"]["calories"], reverse=True)

    return {
        "foods": foods,
        "total": total,
    }


def __get_aggregates_of_journal_for_date(journal: list, catalog: dict) -> dict:
    result = {}

    for entry in journal:
        is_comment = isinstance(entry, str)

        if is_comment:
            continue

        entry_title = tuple(entry)[0]

        entry_title_from_catalog = __get_food_title_from_catalog(catalog, entry_title)

        pattern = re.compile("^[ 0-9\\+\\-()/*]+$")

        if entry_title_from_catalog is not None:
            try:
                entry_grams = str(tuple(entry.values())[0])

                if pattern.search(entry_grams) is None:
                    raise ValueError

                entry_grams = eval(entry_grams)  # pylint: disable=eval-used

            except (SyntaxError, ZeroDivisionError):
                # SyntaxError:          "1+2)+3"
                # ZeroDivisionError:    "1/0"

                print(f'Unable to get weight for the journal\'s entry "{entry_title}".')
                entry_grams = 0

            if result.get(entry_title_from_catalog) is None:
                result[entry_title_from_catalog] = entry_grams
            else:
                result[entry_title_from_catalog] += entry_grams

        else:
            print(f'Catalog\'s entry "{entry_title}" is not found.')

    return result


def __get_food_title_from_catalog(catalog: dict, food_title: str) -> dict:
    result = None

    for catalog_item in catalog:
        if catalog_item.lower() == food_title.lower():
            if isinstance(catalog[catalog_item], str):
                result = __get_food_title_from_catalog(catalog, catalog[catalog_item])
            else:
                result = catalog_item
            break

    return result


def __get_food(foods: list, food_title: str) -> dict:
    foods_list = list(filter(lambda x: x["title"] == food_title, foods))

    return foods_list[0] if len(foods_list) > 0 else None


def __get_food_template(food_title: str) -> dict:
    return {"title": food_title, "total": __get_total_template()}


def __get_total_template() -> dict:
    return {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "grams": 0,
    }


def nutrients_balance(total: dict) -> dict:
    """
    Returns nutrients balance.
    """

    nutrients_total = total["protein"] + total["fat"] + total["carbs"]

    return {
        "protein_percent": __percent(nutrients_total, total["protein"]),
        "fat_percent": __percent(nutrients_total, total["fat"]),
        "carbs_percent": __percent(nutrients_total, total["carbs"]),
    }


def __percent(total: int, value: int) -> int:
    if total > 0:
        result = round(value * 100 / total)
    else:
        result = 0

    return result
