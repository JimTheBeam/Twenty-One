from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


# keyboard:
def my_keyboard():
    keyboard = ReplyKeyboardMarkup([['Play Game!'], ['Help!', 'Liderboard']], resize_keyboard=True)
    return keyboard

def game_keyboard():
    keyboard = ReplyKeyboardMarkup([['Another card', 'Enough'], ['Quit game']], resize_keyboard=True)
    return keyboard



