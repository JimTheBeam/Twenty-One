from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


# keyboard:
def my_keyboard():
    keyboard = ReplyKeyboardMarkup([['Play Twenty-one', 'Play TicTacToe'], 
                                    ['Liderboard for 21', 'Liderboard for TicTacToe'],
                                    ['Help!']], 
                                    resize_keyboard=True)
    return keyboard

def game_keyboard():
    keyboard = ReplyKeyboardMarkup([['Another card', 'Enough'], 
                                    ['Quit game']], 
                                    resize_keyboard=True)
    return keyboard


def start_keyboard():
    keyboard = ReplyKeyboardMarkup([['cancel']],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return keyboard

