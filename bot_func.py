import logging

from telegram.ext import ConversationHandler

from keyboard import my_keyboard, game_keyboard, start_keyboard

from database.work_with_db import insert_start_data_liderboard_21

# this func works when command /start
def start(update, context):
    """Send a message when the command /start is issued."""
    logging.info('/start')
    text = 'Hi! In this bot you can play games twenty-one and tictactoe! '\
            'Press /help for help if needed.'
    update.message.reply_text(text, reply_markup=my_keyboard())

    # анька фикс
    chat = update.message.chat
    if chat.first_name == None:
        text = 'Your account don\'t have username and first name. \n'\
            'If you want to be in liderboard table send your nickname in response.\n'\
            'If not just press "cancel" on keyboard below'
        update.message.reply_text(text=text, reply_markup=start_keyboard())
        return 'NICKNAME'
    else:
        return ConversationHandler.END


def add_nickname(update, context):
    chat = update.message.chat
    nickname = update.message.text
    chat_id = chat.id
    username = chat.username
    first_name = chat.first_name
    last_name = chat.last_name
    # insert data in database:
    insert_start_data_liderboard_21(chat_id, username, first_name, last_name, nickname=nickname)

    # send message to user:
    text = f'Your nickname {nickname} was added into the base. '\
         'You\'ll be able to see yourself in the liderboard now!'
    update.message.reply_text(text=text,reply_markup=my_keyboard())
    return ConversationHandler.END


def cancel_nickname(update, context):
    chat = update.message.chat
    logging.info(f'user with chat_id: {chat.id} don\'t want enter nickname')
    text = 'Sadly :-( \n If you decide to chage your mind send me command /start'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END


def wrong_nickname(update, context):
    logging.info('func wrong_nickname is started')
    text = 'I don\'t understand you. Send me your nickname if you want to be in liderboard '\
            'or press "cancel" if you don\'t'
    update.message.reply_text(text, reply_markup=start_keyboard())
    return 'NICKNAME'


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
    update.message.reply_text(text, reply_markup=my_keyboard())


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