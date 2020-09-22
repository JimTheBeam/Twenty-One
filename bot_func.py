import logging

from telegram.ext import ConversationHandler

from keyboard import my_keyboard, game_keyboard

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
    logging.info('/help')
    text = '''The aim is to score exactly twenty-one points \
or to come as close to twenty-one as possible, \
based on the card values dealt.

The numeral cards 6 to 10 have their face values,
Jacks valued at 2,
Queens valued at 3,
Kings valued at 4,
Aces valued at 11'''
    update.message.reply_text(text)


def wrong_in_game(update, context):
    logging.info('func wrong_in_game is started')
    text = "I don't understand you. Try something else."
    update.message.reply_text(text, reply_markup=game_keyboard())
    return 'GAME'


def wrong(update, context):
    logging.info('func wrong is started')
    text = "I don't understand you. Try something else."
    update.message.reply_text(text, reply_markup=my_keyboard())


# stops conversation handler and the Game
def stop(update, context):
    text = 'Game over'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END