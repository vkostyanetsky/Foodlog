import os
import datetime

import modules.yaml_wrapper as yaml_wrapper

def get_daily_calories_limit(dirpath, options):

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