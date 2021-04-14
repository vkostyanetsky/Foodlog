import os
import yaml
import datetime

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

            message = 'ОШИБКА: не удалось обработать запись журнала "{}"!'.format(entry)
            exit(message)

        item, weight = fields

        if weights.get(item) == None:
            weights[item] = 0
        
        weights[item] += weight    

    return weights

def get_consumption(parameter):

    details     = []
    value_total = 0

    for item in weights:

        value = round(weights[item] * catalog[item][parameter] / 100)

        details.append((item, value))

        value_total += value

    details.sort(key = lambda i: i[1], reverse = True)    

    return [details, value_total]

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
dirpath         = os.path.split(script_dirpath)[0]

options = common_logic.get_settings(script_dirpath)
catalog = get_catalog()
journal = get_journal()
weights = get_weights()

calories, calories_total = get_consumption('К')
  
item_offset = get_max_item_length()

if len(calories) > 0:

    print('ПРОДУКТ'.ljust(item_offset), 'К')

    print()

    for item, value in calories:
        print(item.ljust(item_offset), value)

    print()

    print('ИТОГО'.ljust(item_offset), calories_total)
    
else:

    print('Журнал за день пуст!')