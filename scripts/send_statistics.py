import os
import random
import hashlib
import requests

import modules.common_logic     as common_logic
import modules.journal_reader   as journal_reader

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

    with open(options['journal_filepath'], 'rb') as file:
        
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

def get_random_food_related_emoji():

    smilies = [
        '🍏', '🍎', '🍐', '🍊', '🍋',
        '🍌', '🍉', '🍇', '🍓', '🍈',
        '🍒', '🍑', '🥭', '🍍', '🥥',
        '🥝', '🍅', '🍆', '🥑', '🥦',
        '🥬', '🥒', '🌶', '🌽', '🥕',
        '🧄', '🧅', '🥔', '🍠', '🥐',
        '🥯', '🍞', '🥖', '🥨', '🧀',
        '🥚', '🍳', '🧈', '🥞', '🧇',
        '🥓', '🥩', '🍗', '🍖', '🦴',
        '🌭', '🍔', '🍟', '🍕', '🥪',
        '🥙', '🧆', '🌮', '🌯', '🥗',
        '🥘', '🥫', '🍝', '🍜', '🍲',
        '🍛', '🍣', '🍱', '🥟', '🦪',
        '🍤', '🍙', '🍚', '🍘', '🍥',
        '🥠', '🥮', '🍢', '🍡', '🍧',
        '🍨', '🍦', '🥧', '🧁', '🍰',
        '🎂', '🍮', '🍭', '🍬', '🍫',
        '🍿', '🍩', '🍪', '🌰', '🥜', 
        '🍯', '🥛', '🍼', '☕️', '🍵',
        '🧃', '🥤', '🍶', '🍺', '🍻',
        '🥂', '🍷', '🥃', '🍸', '🍹',
        '🧉', '🍾', '🧊', '🥄', '🍴',
        '🍽', '🥣', '🥡', '🥢', '🧂'
    ]

    return random.choice(smilies)

options = common_logic.get_options()

stored_journal_hash_filepath = '{}.md5'.format(options['journal_filepath'])

stored_journal_hash = get_stored_journal_hash()
actual_journal_hash = get_actual_journal_hash()

if stored_journal_hash != actual_journal_hash:

    store_journal_hash(actual_journal_hash)

    catalog = common_logic.get_catalog(options)
    journal = common_logic.get_journal(options)

    statistics = journal_reader.get_statistics(journal, catalog, options)
    
    if statistics['calories_to_consume'] >= 0:

        message = 'Сегодня получено {} ккал из {}! Остаток: {} {}'

    else:

        message = 'Сегодня получено {} ккал из {}! Избыток: {} {}'
        statistics['calories_to_consume'] *= -1

    emoji = get_random_food_related_emoji()

    message = message.format(
        statistics['calories_total'],
        statistics['calories_limit'],
        statistics['calories_to_consume'],
        emoji
    )

    send_to_telegram(message)