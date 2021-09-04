import os
import hashlib
import requests

import modules.common_logic         as common_logic
import modules.journal_reader       as journal_reader
import modules.limits_calculator    as limits_calculator

def store_journal_hash(hash):

    with open(stored_journal_hash_filepath, 'w') as hash_file:
        hash_file.write(hash)

def get_stored_journal_hash():

    try:

        handle = open(stored_journal_hash_filepath, 'r')
        result = handle.readline()
        handle.close()

    except:

        result = None

    return result

def get_actual_journal_hash():

    buffer_size = 65536
    md5         = hashlib.md5()

    with open(journal_filepath, 'rb') as file:
        
        while True:

            data = file.read(buffer_size)

            if not data:
                break

            md5.update(data)

    return md5.hexdigest()

def send_to_telegram(text: str):

    url = 'https://api.telegram.org/bot'
    url += options['telegram_bot_api_token']
    url += '/sendMessage'

    data = {
        'chat_id':  options['telegram_chat_id'],
        'text':     text
    }

    result = requests.post(url, data)

    if result.status_code != 200:
        raise Exception('Unable to send a message via Telegram!')

scripts_dirpath = os.path.abspath(os.path.dirname(__file__))

dirpath = os.path.split(scripts_dirpath)[0]
options = common_logic.get_options(dirpath)

journal_filepath                = os.path.join(dirpath, options['journal_filename'])
stored_journal_hash_filepath    = '{}.md5'.format(journal_filepath)

stored_journal_hash = get_stored_journal_hash()
actual_journal_hash = get_actual_journal_hash()

if stored_journal_hash != actual_journal_hash:

    store_journal_hash(actual_journal_hash)

    catalog = common_logic.get_catalog(dirpath, options)
    journal = common_logic.get_journal(dirpath, options)

    statistics = journal_reader.get_statistics(journal, catalog)
    daily_kcal = limits_calculator.get_daily_calories_limit(dirpath, options)
    
    message = 'Сегодня съедено {} ккал из {}! 🥣'.format(statistics['calories_total'], daily_kcal)
    send_to_telegram(message)