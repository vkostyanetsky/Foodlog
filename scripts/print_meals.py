import os
import operator
import datetime

import modules.common_logic as common_logic
import modules.yaml_wrapper as yaml_wrapper

def get_journal():

    journal_filepath = os.path.join(dirpath, settings['journal_filename'])

    result = yaml_wrapper.get_data_from_file(journal_filepath)
    
    if result == None:
        result = []
                
    return result

def get_catalog():

    catalog_filepath = os.path.join(dirpath, settings['catalog_filename'])

    return yaml_wrapper.get_data_from_file(catalog_filepath)
    
def get_max_item_length():

    result = 0

    for item in catalog:
        length = len(item)

        if length > result:
            result = length

    return result + 3

def get_calculated_calories_limit():

    def get_basal_metabolic_rate():

        def get_body_weight():

            def get_body_weights():

                weights_filepath = os.path.join(dirpath, settings['weights_filename'])

                return yaml_wrapper.get_data_from_file(weights_filepath)

            body_weights = get_body_weights()

            if len(body_weights) > 0:
                result = list(body_weights[-1].items())[0][1]
            else:
                result = 0

            return float(result)

        def get_age():

            days_in_year    = 365.2425
            birth_date      = datetime.datetime.strptime(settings['birth_date'], '%d.%m.%Y').date()

            result = (datetime.date.today() - birth_date).days / days_in_year
            
            return int(result)

        weight  = get_body_weight()
        height  = settings['height']
        age     = get_age()
    
        # https://en.wikipedia.org/wiki/Harris–Benedict_equation

        result = (10 * weight) + (6.25 * height) - (5 * age) 

        if settings['sex'] == 'man':
            result +=5
        else:
            result -=161

        return result
    
    basal_metabolic_rate = get_basal_metabolic_rate()
    
    calories = basal_metabolic_rate * settings['activity_multiplier']
    shortage = calories * settings['calories_shortage'] / 100
    
    return round(calories - shortage)

def get_weights():

    def get_entry_fields(entry):

        entry = str(entry)
        index = entry.rfind(',')

        if index != -1:

            item   = entry[0:index]
            weight = int(entry[index + 1:])

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
    
        if nutrients_total > 0:    
            result = round(value * 100 / nutrients_total)
        else:
            result = 0

        result = str(result) + '%'

        return result

    nutrients_total = proteins_total + fats_total + carbohydrates_total

    proteins_percent        = percent(proteins_total)    
    fats_percent            = percent(fats_total)
    carbohydrates_percent   = percent(carbohydrates_total)

    print_table_row('Баланс БЖУ сегодня', '', proteins_percent, fats_percent, carbohydrates_percent)
    print_table_row('Целевой баланс БЖУ', '', '30%', '20%', '50%')    

def print_calories_balance():

    if settings['calories_limit'] > 0:
        calories_limit = settings['calories_limit']
    else:
        calories_limit = get_calculated_calories_limit()

    balance = calories_limit - calories_total

    if balance >= 0:
        balance_message = 'остаток на сегодня — {}.'.format(balance)
    else:
        balance_message = 'превышение — {}!'.format(balance * -1)

    message = 'Дневная норма — {} ккал; {}'.format(calories_limit, balance_message)

    print()
    print(message)

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
settings        = common_logic.get_settings(script_dirpath)

dirpath = os.path.split(script_dirpath)[0]
catalog = get_catalog()
journal = get_journal()
weights = get_weights()

calories, calories_total            = get_consumption('К')
proteins, proteins_total            = get_consumption('Б')
fats, fats_total                    = get_consumption('Ж')
carbohydrates, carbohydrates_total  = get_consumption('У')

item_offset = get_max_item_length()
data_offset = 10

print_table_row('ПРОДУКТ', 'К', 'Б', 'Ж', 'У')
print()

print_nutrients()
print()

print_nutrients_balance()
print_calories_balance()