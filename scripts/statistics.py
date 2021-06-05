import os
import yaml
import datetime
import operator

import modules.common_logic as common_logic
import modules.yaml_wrapper as yaml_wrapper

def get_journal():

    journal_filepath = os.path.join(dirpath, options['journal_filename'])

    result = yaml_wrapper.get_data_from_file(journal_filepath)
    
    if result == None:
        result = []
                
    return result

def get_catalog():

    catalog_filepath = os.path.join(dirpath, options['catalog_filename'])

    return yaml_wrapper.get_data_from_file(catalog_filepath)
    
def get_max_item_length():

    result = 0

    for item in catalog:
        length = len(item)

        if length > result:
            result = length

    return result + 3

def get_weights():

    def get_entry_fields(entry):

        entry   = str(entry)
        fields  = entry.split(',')

        if len(fields) == 2:

            item    = fields[0].strip()
            weight  = int(fields[1].strip())

            result = [item, weight]

        else:

            result = None

        return result

    weights = {}

    for entry in journal:

        fields = get_entry_fields(entry)

        if fields == None:

            message = 'ОШИБКА: не вышло получить продукт и его вес из записи журнала "{}"!'.format(entry)
            exit(message)

        item, weight = fields

        if weights.get(item) == None:
            weights[item] = 0
        
        weights[item] += weight    

    return weights

def get_consumption(parameter):

    details     = {}
    value_total = 0

    for item in weights:

        item_parameters = catalog.get(item)

        if item_parameters != None:

            parameter_value = item_parameters.get(parameter)

            if parameter_value != None:

                value = round(weights[item] * parameter_value / 100)

                details[item] = value

                value_total += value

            else:

                message = 'У продукта "{}" в справочнике не указан параметр "{}"!'.format(item, parameter)
                exit(message)

        else:

            message = 'Продукт "{}" не найден в справочнике!'.format(item)
            exit(message)

    return [details, value_total]

def print_table_row(item, calories_value, proteins_value, fats_value, carbohydrates_value):

    item                    = item.ljust(item_offset)
    calories_value          = str(calories_value).ljust(data_offset)
    proteins_value          = str(proteins_value).ljust(data_offset)
    fats_value              = str(fats_value).ljust(data_offset)
    carbohydrates_value     = str(carbohydrates_value).ljust(data_offset)

    print(item, calories_value, proteins_value, fats_value, carbohydrates_value)

def print_nutrients():

    sorted_calories = sorted(calories.items(), key = operator.itemgetter(1), reverse = True)

    for item, value in sorted_calories:
        print_table_row(item, value, proteins[item], fats[item], carbohydrates[item])

    print()

    print_table_row('ИТОГО', calories_total, proteins_total, fats_total, carbohydrates_total)    

def print_nutrients_balance():

    def percent(value):
    
        result = round(value * 100 / nutrients_total)
        result = str(result) + '%'

        return result

    nutrients_total = proteins_total + fats_total + carbohydrates_total

    proteins_percent        = percent(proteins_total)    
    fats_percent            = percent(fats_total)
    carbohydrates_percent   = percent(carbohydrates_total)

    print_table_row('Баланс БЖУ сегодня', '', proteins_percent, fats_percent, carbohydrates_percent)
    print_table_row('Целевой баланс БЖУ', '', '30%', '20%', '50%')    

def print_calories_balance():

    balance = options['calories_limit'] - calories_total
    message = 'Дневная норма — {} ккал; остаток на сегодня — {}.'.format(options['calories_limit'], balance)

    print()
    print(message)

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
dirpath         = os.path.split(script_dirpath)[0]

options = common_logic.get_options(dirpath)
catalog = get_catalog()
journal = get_journal()
weights = get_weights()

calories, calories_total            = get_consumption('К')
proteins, proteins_total            = get_consumption('Б')
fats, fats_total                    = get_consumption('Ж')
carbohydrates, carbohydrates_total  = get_consumption('У')

item_offset = get_max_item_length()
data_offset = 10

if len(calories) > 0:

    print_table_row('ПРОДУКТ', 'К', 'Б', 'Ж', 'У')

    print()

    print_nutrients()

    print()

    print_nutrients_balance()

    print_calories_balance()

else:

    print('Журнал за день пуст!')