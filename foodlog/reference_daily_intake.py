#!/usr/bin/env python3

"""
Daily calories intake calculator using user's profile given.
"""

from datetime import date


def get_calories_limit(profile: dict, weights: dict) -> int:
    """
    Returns calories limit for a user's profile.
    """

    if profile["calories_limit"] > 0:
        result = profile["calories_limit"]
    else:
        result = __get_calculated_daily_calories_limit(profile, weights)

    return result


def __get_calculated_daily_calories_limit(profile: dict, weights: dict) -> int:
    basal_metabolic_rate = __get_basal_metabolic_rate(profile, weights)

    calories = basal_metabolic_rate * profile["activity_multiplier"]
    shortage = calories * profile["caloric_deficit"] / 100

    return round(calories - shortage)


def __get_body_weight(weights: dict) -> float:
    if len(weights) > 0:
        body_weight = sorted(weights.items(), key=lambda x: x[0])[-1][1]
    else:
        body_weight = 0

    return float(body_weight)


def __get_age(profile: dict) -> int:
    days_in_year = 365.2425
    days_in_life = (date.today() - profile["birth_date"]).days

    return int(days_in_life / days_in_year)


def __get_basal_metabolic_rate(profile: dict, weights: dict) -> int:
    """
    https://en.wikipedia.org/wiki/Harris–Benedict_equation
    """

    weight = __get_body_weight(weights)
    height = profile["height"]

    age = __get_age(profile)
    bmr = (10 * weight) + (6.25 * height) - (5 * age)

    if profile["sex"] == "man":
        bmr += 5
    else:
        bmr -= 161

    return bmr
