def get_statistics(journal, catalog):

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

    weights = get_weights()

    calories, calories_total            = get_consumption('К')
    proteins, proteins_total            = get_consumption('Б')
    fats, fats_total                    = get_consumption('Ж')
    carbohydrates, carbohydrates_total  = get_consumption('У')

    return {
        'calories':             calories,
        'calories_total':       calories_total,
        'proteins':             proteins,
        'proteins_total':       proteins_total,
        'fats':                 fats,
        'fats_total':           fats_total,
        'carbohydrates':        carbohydrates,
        'carbohydrates_total':  carbohydrates_total,
    }