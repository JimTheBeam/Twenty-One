from telegram import InlineKeyboardButton, InlineKeyboardMarkup,\
                    ReplyKeyboardMarkup, ReplyKeyboardRemove


# keyboard:
def my_keyboard():
    keyboard = ReplyKeyboardMarkup([['Play Game!'], ['help!', 'STOP']], resize_keyboard=True)
    return keyboard

def game_keyboard():
    keyboard = ReplyKeyboardMarkup([['Another card', 'Enough'], ['STOP']], resize_keyboard=True)
    return keyboard


def file_keyboard():
    keyboard = ReplyKeyboardMarkup([['STOP']], resize_keyboard=True)
    return keyboard
