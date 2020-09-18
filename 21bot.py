import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup

import settings

from keyboard import my_keyboard, game_keyboard

from twentyone_logic import start_game, game, stop, enough

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

logging.info('bot started')

logger = logging.getLogger(__name__)


# this func works when command /start
def start(update, context):
    """Send a message when the command /start is issued."""
    logging.info('/start')
    text = 'Hi! This bot was created for playing game 21!'
    text2 = 'Press /help for help if needed.'
    update.message.reply_text(text, reply_markup=my_keyboard())
    update.message.reply_text(text2, reply_markup=my_keyboard())


# answers to /help command
def help_command(update, context):
    """Send a message when the command /help is issued."""
    text = '''The aim is to score exactly twenty-one points \
or to come as close to twenty-one as possible, \
based on the card values dealt.
The numeral cards 6 to 10 have their face values,
Jacks valued at 2,
Queens valued at 3,
Kings valued at 4,
Aces valued at 11'''
    update.message.reply_text(text)


def wrong(update, context):
    text = "I don't understand you. Try something else."
    update.message.reply_text(text, reply_markup=my_keyboard())


def main():
    """Start the bot."""
    updater = Updater(settings.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("id", add_telegram_id_in_sql))
    dp.add_handler(MessageHandler(Filters.regex('^(Help!)$'), help_command))
    # dp.add_handler(MessageHandler(Filters.regex('^(Quit game)$'), stop))

    game_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Play Game!)$'), start_game)],
            states={
                'GAME': [MessageHandler(Filters.regex('^(Another card)$'), game),
                        MessageHandler(Filters.regex('^(Enough)$'), enough)]
            },
            fallbacks=[MessageHandler(Filters.regex('^(Quit game)$'), stop),
            CommandHandler('start', start)]
            )
    dp.add_handler(game_handler)

    dp.add_handler(MessageHandler(Filters.all, wrong))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

__version__ = '1.0.1'