import datetime as datetime

import modules.common_logic as common_logic
import modules.yaml_wrapper as yaml_wrapper

def get_entries(path):

    return yaml_wrapper.get_data_from_file(path)

def put_entries(path, data):

    yaml_wrapper.put_data_to_file(path, data)

def is_fasting_started(journal_entries):

    if len(journal_entries) == 0:
        result      = False
    else:
        last_entry  = journal_entries[-1]
        result      = len(last_entry) == 2

    return result

def get_length(entry):
    
    start_date = entry[1]
    
    if len(entry) == 2:
        end_date = datetime.datetime.today()
    else:
        end_date = entry[2]

    seconds = (end_date - start_date).total_seconds()
    hours   = int(seconds / 60 / 60)
    minutes = int((seconds - hours * 60 * 60) / 60)

    return [hours, minutes]

def start_fasting(length):

    arguments   = common_logic.get_arguments()
    settings    = yaml_wrapper.get_data_from_file(arguments.settings)
    entries     = get_entries(settings['fasting_journal_filepath'])
    message     = ''

    if is_fasting_started(entries):

        message = 'Голодание уже начато.'

    else:
        
        if length.isdigit():
            
            length      = int(length)
            start_date  = datetime.datetime.today()
            new_entry   = [length, start_date] 

            entries.append(new_entry)

            put_entries(settings['fasting_journal_filepath'], entries)    

        else:

            message = 'Продолжительность голодания должна быть целым числом.'

    return message

def stop_fasting():

    arguments   = common_logic.get_arguments()
    settings    = yaml_wrapper.get_data_from_file(arguments.settings)
    entries     = get_entries(settings['fasting_journal_filepath'])
    message     = ''

    if is_fasting_started(entries):

        last_entry  = entries[-1]
        end_date    = datetime.datetime.today()

        last_entry.append(end_date)

        put_entries(settings['fasting_journal_filepath'], entries)

        length = get_length(last_entry)

        message = "Голодание завершено! Ожидаемая продолжительность: {} часов, фактическая — {} часов {} минут.".format(last_entry[0], length[0], length[1])

    else:

        message = "Голодание не начато."

    return message

def prettydate(start_date):

    def day():

        if start_date.month == 1:
            month_name = 'января'
        elif start_date.month == 2:
            month_name = 'февраля'
        elif start_date.month == 3:
            month_name = 'марта'
        elif start_date.month == 4:
            month_name = 'апреля'
        elif start_date.month == 5:
            month_name = 'мая'
        elif start_date.month == 6:
            month_name = 'июня'
        elif start_date.month == 7:
            month_name = 'июля'
        elif start_date.month == 8:
            month_name = 'августа'
        elif start_date.month == 9:
            month_name = 'сентября'
        elif start_date.month == 10:
            month_name = 'октября'
        elif start_date.month == 11:
            month_name = 'ноября'
        elif start_date.month == 12:
            month_name = 'декабря'

        return '{} {}'.format(start_date.day, month_name)

    now = datetime.datetime.today()

    if start_date.year == now.year and start_date.month == now.month and now.day - start_date.day == 1:
        day = 'вчера'
    else:
        day = day()

    time = start_date.strftime('%H:%M')

    return '{} в {}'.format(day, time)

def get_fasting_info():

    arguments   = common_logic.get_arguments()
    settings    = yaml_wrapper.get_data_from_file(arguments.settings)
    entries     = get_entries(settings['fasting_journal_filepath'])
    message     = ''

    if is_fasting_started(entries):

        last_entry  = entries[-1]
        length      = get_length(last_entry)

        d = prettydate(last_entry[1])

        message = "Голодание началось {} и длится {} часа и {} минуты. Ожидаемая продолжительность — {} часов.".format(d, length[0], length[1], last_entry[0])

    else:

        message = "Сейчас голодание не идёт."
        
    return message