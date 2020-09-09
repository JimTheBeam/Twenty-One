import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup

import settings

from keyboard import my_keyboard, game_keyboard

from twentyone_logic import start_game, game, stop, check_photo, file_name

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
    update.message.reply_text('Help!')


# FIXME: need to del this func
# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

    


def main():
    """Start the bot."""
    updater = Updater(settings.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))


    # get file_ID
    # dp.add_handler(MessageHandler(Filters.photo, check_photo))
    photo_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.photo, check_photo)],
            states={
                'File name': [MessageHandler(Filters.text, file_name)]
            },
            fallbacks=[MessageHandler(Filters.regex('^(STOP)$'), stop),
            CommandHandler('start', start)]
    )
    dp.add_handler(photo_handler)


    game_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Play Game!)$'), start_game)],
            states={
                'GAME': [MessageHandler(Filters.regex('^(Play Game!)$'), game)]
            },
            fallbacks=[MessageHandler(Filters.regex('^(STOP)$'), stop),
            CommandHandler('start', start)]
            )
    dp.add_handler(game_handler)


    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()