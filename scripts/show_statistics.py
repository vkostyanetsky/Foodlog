import operator

import modules.common_logic     as common_logic
import modules.yaml_wrapper     as yaml_wrapper
import modules.journal_reader   as journal_reader
    
def get_max_item_length():

    result = 0

    for item in catalog:
        length = len(item)

        if length > result:
            result = length

    return result + 3

def print_table_row(item, calories_value, proteins_value, fats_value, carbohydrates_value):

    item                    = item.ljust(item_offset)
    calories_value          = str(calories_value).ljust(data_offset)
    proteins_value          = str(proteins_value).ljust(data_offset)
    fats_value              = str(fats_value).ljust(data_offset)
    carbohydrates_value     = str(carbohydrates_value).ljust(data_offset)

    print(item, calories_value, proteins_value, fats_value, carbohydrates_value)

def print_nutrients():

    sorted_calories = sorted(statistics['calories'].items(), key = operator.itemgetter(1), reverse = True)

    for item, value in sorted_calories:
        print_table_row(item, value, statistics['proteins'][item], statistics['fats'][item], statistics['carbohydrates'][item])

    print()

    print_table_row('ИТОГО', statistics['calories_total'], statistics['proteins_total'], statistics['fats_total'], statistics['carbohydrates_total'])

def print_nutrients_balance():

    def percent(value):
    
        if nutrients_total > 0:    
            result = round(value * 100 / nutrients_total)
        else:
            result = 0

        result = str(result) + '%'

        return result

    def default_percent(value):

        return '{}%'.format(value)

    nutrients_total = statistics['proteins_total'] + statistics['fats_total'] + statistics['carbohydrates_total']

    proteins_percent        = percent(statistics['proteins_total'])
    fats_percent            = percent(statistics['fats_total'])
    carbohydrates_percent   = percent(statistics['carbohydrates_total'])

    default_proteins_percent        = default_percent(options['proteins_percent'])
    default_fats_percent            = default_percent(options['fats_percent'])
    default_carbohydrates_percent   = default_percent(options['carbohydrates_percent'])

    print_table_row('Баланс БЖУ сегодня', '', proteins_percent, fats_percent, carbohydrates_percent)
    print_table_row('Целевой баланс БЖУ', '', default_proteins_percent, default_fats_percent, default_carbohydrates_percent)

def print_calories_balance():

    if statistics['calories_to_consume'] >= 0:
        balance_message = 'остаток на сегодня — {}.'.format(statistics['calories_to_consume'])
    else:
        balance_message = 'превышение — {}!'.format(statistics['calories_to_consume'] * -1)

    message = 'Дневная норма — {} ккал; {}'.format(statistics['calories_limit'], balance_message)

    print()
    print(message)

options = common_logic.get_options()
catalog = common_logic.get_catalog(options)
journal = common_logic.get_journal(options)

statistics = journal_reader.get_statistics(journal, catalog, options)

item_offset = get_max_item_length()
data_offset = 10

print_table_row('ПРОДУКТ', 'К', 'Б', 'Ж', 'У')
print()

print_nutrients()
print()

print_nutrients_balance()
print_calories_balance()