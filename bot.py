import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton,\
                    InlineKeyboardMarkup, ReplyKeyboardRemove

import settings

from keyboard import my_keyboard, game_keyboard

from twentyone_logic import start_game, game, enough, liderboard

from bot_func import start, help_command, wrong, wrong_in_game, stop

from tictac.tictac_game_logic import start_game_tictac, game_tictac 


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

logging.info('bot started')
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    updater = Updater(settings.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    twenty_one_game_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Play Twenty-one)$'), start_game)],
            states={
                'GAME': [MessageHandler(Filters.regex('^(Another card)$'), game),
                        MessageHandler(Filters.regex('^(Enough)$'), enough)]
            },
            fallbacks=[MessageHandler(Filters.regex('^(Quit game)$'), stop),
            MessageHandler(Filters.all, wrong_in_game)]
            )
    dp.add_handler(twenty_one_game_handler)

    tictac_game_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Play TicTacToe)$'), start_game_tictac)],
            states={
                'GAME' : [CallbackQueryHandler(game_tictac)]
            },
            fallbacks=[MessageHandler(Filters.regex('^(Play TicTacToe)$'), start_game_tictac),
            CommandHandler('start', start)]
            )
    dp.add_handler(tictac_game_handler)


    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.regex('^(Help!)$'), help_command))
    dp.add_handler(MessageHandler(Filters.regex('^(Liderboard for 21)$'), liderboard))

    dp.add_handler(MessageHandler(Filters.all, wrong))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

__version__ = '1.0.3'