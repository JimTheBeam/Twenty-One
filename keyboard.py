from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


# keyboard:
def my_keyboard():
    keyboard = ReplyKeyboardMarkup([['Play Twenty-one', 'Play TicTacToe'], 
                                    ['Help!', 'Liderboard for 21']], 
                                    resize_keyboard=True)
    return keyboard

def game_keyboard():
    keyboard = ReplyKeyboardMarkup([['Another card', 'Enough'], 
                                    ['Quit game']], 
                                    resize_keyboard=True)
    return keyboard



