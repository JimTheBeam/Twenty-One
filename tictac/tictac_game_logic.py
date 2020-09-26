from telegram.ext import Updater, ConversationHandler

from tictac.keyboards_tictac import tictac_keyb, error_keyboard, inline_keys,\
    text_x, text_o, text_none

from random import randint


# starts the game 
def start_game_tictac(update, context):
    user_data = context.user_data

    user_data['buttons'] = inline_keys()

    update.message.reply_text(text='Game started',
                         reply_markup=tictac_keyb(*user_data['buttons']))

    return 'GAME'


def add_o_if_two_in_row(button, text):
    """[add 'O' on the field to block user's two 'X'
    or add 'O' to win the game]

    Args:
        button ([list]): [list of buttons from the game]
        text ([str]): [can be 'text_o' or 'text_x'. 
            It's a parameter to check if two in a row]

    Returns:
        [button]: [list of buttons with added 'O']
    """
    lines = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for i in lines:
        if button[i[0]] == button[i[1]] == text or\
            button[i[0]] == button[i[2]] == text or\
            button[i[1]] == button[i[2]] == text:
            for f in i:
                if button[f] == text_none:
                    button[f] = text_o
                    return button


# check if there are two 'O' or 'X' in one row and one vacant place
# return True or False
def check_two_in_row(button, text):
    lines = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for i in lines:
        if button[i[0]] == button[i[1]] == text or\
            button[i[0]] == button[i[2]] == text or\
            button[i[1]] == button[i[2]] == text:
            for f in i:
                if button[f] == text_none:
                    return True
    return False


# func add 'O' in game keyboard
def add_o(button):
    if check_two_in_row(button, text_o):
        button = add_o_if_two_in_row(button, text_o)
        return button
    else:
        if check_two_in_row(button, text_x):
            button = add_o_if_two_in_row(button, text_x)
            return button
        else:
            while True:
                # add 'O' randomly
                random_index_o = randint(0,8)
                # check if random index is free
                if button[random_index_o] == text_none:
                    button[random_index_o] = text_o
                    return button


# check if user won. (3 in a row)
def check_user_win(button):
    lines = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in lines:
        if button[each[0]] == button[each[1]] == button[each[2]] == text_x:
            return True
    return False


# check if bot won. (3 in a row)
def check_bot_win(button):
    lines = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in lines:
        if button[each[0]] == button[each[1]] == button[each[2]] == text_o:
            return True
    return False


# main function of the game
# catch if inline keyboard button is pressed
def game_tictac(update, context):
    query = update.callback_query
    user_data = context.user_data

    # check if user_data has buttons for keyboard
    if not 'buttons' in user_data:
        user_data['buttons'] = inline_keys()
    else:
        button = user_data['buttons']

    # add user's X to keyboard
    try:
        user_choice = int(query.data)
        if button[user_choice] == text_none:
            button[user_choice] = text_x
        else:
            context.bot.edit_message_text(text='Wrong cell', chat_id=query.message.chat_id, 
                message_id=query.message.message_id,
                reply_markup=tictac_keyb(*button))
            return 'GAME'
    except TypeError:
        keyboard = error_keyboard()

    # check if user won. (3 in a row)
    if check_user_win(button) == False:
        pass
    else:
        context.bot.edit_message_text(text='You won!',
                chat_id=query.message.chat_id, 
                message_id=query.message.message_id)
        return ConversationHandler.END

    # check if fild is full:
    if not text_none in button:
        context.bot.edit_message_text(text='Draw!',
                chat_id=query.message.chat_id, 
                message_id=query.message.message_id)
        return ConversationHandler.END

    # bot add 'O' to keyboard
    button = add_o(button)
    keyboard = tictac_keyb(*button)

    # check if bot won. (3 in a row)
    if check_bot_win(button) == False:
        pass
    else:
        context.bot.edit_message_text(text='Bot won!',
                chat_id=query.message.chat_id, 
                message_id=query.message.message_id)
        return ConversationHandler.END

    context.bot.edit_message_text(text='Your turn', chat_id=query.message.chat_id, 
                message_id=query.message.message_id,
                reply_markup=keyboard)
    return 'GAME'
