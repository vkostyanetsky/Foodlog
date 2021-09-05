import os
import datetime

import modules.yaml_wrapper as yaml_wrapper

def get_statistics(journal, catalog, dirpath, options):

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

    def get_calories_limit():

        def get_calculated_daily_calories_limit():

            def get_basal_metabolic_rate():

                def get_body_weight():

                    def get_body_weights():

                        weights_filepath = os.path.join(dirpath, options['weights_filename'])

                        return yaml_wrapper.get_data_from_file(weights_filepath)

                    body_weights = get_body_weights()

                    if len(body_weights) > 0:
                        result = list(body_weights[-1].items())[0][1]
                    else:
                        result = 0

                    return float(result)

                def get_age():

                    days_in_year    = 365.2425
                    birth_date      = datetime.datetime.strptime(options['birth_date'], '%d.%m.%Y').date()

                    result = (datetime.date.today() - birth_date).days / days_in_year
                    
                    return int(result)

                weight  = get_body_weight()
                height  = options['height']
                age     = get_age()
            
                # https://en.wikipedia.org/wiki/Harris–Benedict_equation

                result = (10 * weight) + (6.25 * height) - (5 * age) 

                if options['sex'] == 'man':
                    result += 5
                else:
                    result -= 161

                return result
            
            basal_metabolic_rate = get_basal_metabolic_rate()
            
            calories = basal_metabolic_rate * options['activity_multiplier']
            shortage = calories * options['calories_shortage'] / 100
            
            return round(calories - shortage)

        if options['calories_limit'] > 0:
            result = options['calories_limit']
        else:
            result = get_calculated_daily_calories_limit()

        return result    

    weights = get_weights()

    calories, calories_total            = get_consumption('К')
    proteins, proteins_total            = get_consumption('Б')
    fats, fats_total                    = get_consumption('Ж')
    carbohydrates, carbohydrates_total  = get_consumption('У')

    calories_limit = get_calories_limit()

    return {
        'calories_to_consume':  calories_limit - calories_total,
        'calories_limit':       calories_limit,
        'calories':             calories,
        'calories_total':       calories_total,
        'proteins':             proteins,
        'proteins_total':       proteins_total,
        'fats':                 fats,
        'fats_total':           fats_total,
        'carbohydrates':        carbohydrates,
        'carbohydrates_total':  carbohydrates_total,
    }