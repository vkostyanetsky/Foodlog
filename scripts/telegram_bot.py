#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging
import random

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import modules.fasting_journal_wrapper as fasting_journal_wrapper
import modules.journal_reader   as journal_reader
import modules.common_logic as common_logic
import modules.yaml_wrapper as yaml_wrapper

logging.basicConfig(
    format  = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level   = logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет!')

def start_fasting(update: Update, context: CallbackContext) -> None:

    try:

        fasting_length = int(context.args[0])

        text = fasting_journal_wrapper.start_fasting(fasting_length)

        if text == '':
            text = 'Голодание начато. Так держать!'

        update.message.reply_text(text)

    except (IndexError, ValueError):

        update.message.reply_text('Usage: /newfast <hours>')

def stop_fasting(update: Update, context: CallbackContext) -> None:

    try:

        text = fasting_journal_wrapper.stop_fasting()

        if text != '':
            update.message.reply_text(text)

    except (IndexError, ValueError):

        update.message.reply_text('Usage: /endfast')

def show_fasting_info(update: Update, context: CallbackContext) -> None:

    try:

        text = fasting_journal_wrapper.get_fasting_info()

        update.message.reply_text(text)

    except (IndexError, ValueError):

        update.message.reply_text('Usage: /fastinfo')        

def show_intake(update: Update, context: CallbackContext) -> None:

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

    arguments   = common_logic.get_arguments()
    settings    = yaml_wrapper.get_data_from_file(arguments.settings)

    catalog = common_logic.get_catalog(settings)
    journal = common_logic.get_journal(settings)

    statistics = journal_reader.get_statistics(journal, catalog, settings)
    
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

    update.message.reply_text(message)

def main() -> None:

    arguments   = common_logic.get_arguments()
    settings    = yaml_wrapper.get_data_from_file(arguments.settings)

    updater = Updater(settings['telegram_bot_api_token'])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("newfast", start_fasting))
    dispatcher.add_handler(CommandHandler("endfast", stop_fasting))
    dispatcher.add_handler(CommandHandler("fastinfo", show_fasting_info))
    dispatcher.add_handler(CommandHandler("intake", show_intake))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()