from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove


# inline keyboards:
# buttons:
text_none = '_'
text_o = 'O'
text_x = 'X'


# keyboards:
def error_keyboard():
    button = [[InlineKeyboardButton('Что-то пошло не так', callback_data=0)]]
    keyboard = InlineKeyboardMarkup(button)
    return keyboard


def inline_keys(bt1=text_none, bt2=text_none, bt3=text_none, bt4=text_none, bt5=text_none, 
        bt6=text_none, bt7=text_none, bt8=text_none, bt9=text_none):
    buttons = [bt1, bt2, bt3, 
               bt4, bt5, bt6,
               bt7, bt8, bt9]
    return buttons


def tictac_keyb(*args):
    button1 = InlineKeyboardButton(args[0], callback_data='0')
    button2 = InlineKeyboardButton(args[1], callback_data='1')
    button3 = InlineKeyboardButton(args[2], callback_data='2')
    button4 = InlineKeyboardButton(args[3], callback_data='3')
    button5 = InlineKeyboardButton(args[4], callback_data='4')
    button6 = InlineKeyboardButton(args[5], callback_data='5')
    button7 = InlineKeyboardButton(args[6], callback_data='6')
    button8 = InlineKeyboardButton(args[7], callback_data='7')
    button9 = InlineKeyboardButton(args[8], callback_data='8')
    
    buttons = [
        [button1, button2, button3], 
        [button4, button5, button6],
        [button7, button8, button9]
        ]

    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard



