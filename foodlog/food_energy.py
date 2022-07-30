def get_food_energy(journal: list, catalog: dict) -> tuple:
    total = __get_total_template()
    foods = []

    aggregates = __get_aggregates_of_journal_for_date(journal, catalog)

    for title, grams in aggregates.items():

        food = __get_food(foods, title)

        if food is None:
            foods.append(__get_food_template(title))
            food = foods[-1]

        attribute_values = catalog[title]

        for attribute in ("calories", "protein", "fat", "carbs"):
            value = round(grams * attribute_values[attribute] / 100)

            food["total"][attribute] += value

            total[attribute] += value

    foods = sorted(
        foods, key=lambda x: x["total"]["calories"], reverse=True
    )

    return foods, total


def __get_aggregates_of_journal_for_date(journal: list, catalog: dict) -> dict:
    result = {}

    for entry in journal:

        is_comment = isinstance(entry, str)

        if is_comment:
            continue

        entry_title = tuple(entry)[0]

        entry_title_from_catalog = __get_food_title_from_catalog(catalog, entry_title)

        if entry_title_from_catalog is not None:

            entry_grams = tuple(entry.values())[0]

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
                result = __get_food_title_from_catalog(
                    catalog, catalog[catalog_item]
                )
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
    }
