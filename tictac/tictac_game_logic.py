from telegram.ext import Updater, ConversationHandler

from random import randint

from tictac.keyboards_tictac import tictac_keyb, error_keyboard, inline_keys,\
    text_x, text_o, text_none

from database.work_with_db import update_table_liderboard_tictac,\
            get_games_count_liderboard_tictac, insert_start_data_liderboard_tictac,\
            get_top10_liderboard_tictac

from twentyone_logic import check_liderboard_name

from keyboard import my_keyboard



# starts the game 
def start_game_tictac(update, context):
    user_data = context.user_data

    chat = update.message.chat
    chat_id = chat.id
    # try to get data from liderboard_tictac:
    data = get_games_count_liderboard_tictac(chat_id)
    if not data:
        username = chat.username
        first_name = chat.first_name
        last_name = chat.last_name

        insert_start_data_liderboard_tictac(chat_id, username, first_name, last_name)

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

    chat = query.message.chat
    chat_id = chat.id
    username = chat.username
    first_name = chat.first_name
    last_name = chat.last_name

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
            context.bot.edit_message_text(text='Wrong cell', chat_id=chat_id, 
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
                chat_id=chat_id, 
                message_id=query.message.message_id)
        # get win_count from liderboard_tictac
        games_count = get_games_count_liderboard_tictac(chat_id)    
        if games_count == None:
            win_count = 1
        else:
            if games_count[1] == None:
                win_count = 1
            else:
                win_count = games_count[1] + 1
        # insert win_count in liderboard_tictac
        update_table_liderboard_tictac(chat_id, username, first_name, \
                                last_name, 'win_count', win_count)
        return ConversationHandler.END

    # check if fild is full:
    if not text_none in button:
        context.bot.edit_message_text(text='Draw!',
                chat_id=chat_id, 
                message_id=query.message.message_id)

        games_count = get_games_count_liderboard_tictac(chat_id)
        if games_count == None:
            draw_count = 1
        else:
            if games_count[3] == None:
                draw_count = 1
            else:
                draw_count = games_count[3] + 1
        update_table_liderboard_tictac(chat_id, username, first_name, \
                        last_name, 'draw_count', draw_count)
        return ConversationHandler.END

    # bot add 'O' to keyboard
    button = add_o(button)
    keyboard = tictac_keyb(*button)

    # check if bot won. (3 in a row)
    if check_bot_win(button) == False:
        pass
    else:
        context.bot.edit_message_text(text='Bot won!',
                chat_id=chat_id, 
                message_id=query.message.message_id)

        games_count = get_games_count_liderboard_tictac(chat_id)
        if games_count == None:
            lose_count = 1
        else:
            if games_count[2] == None:
                lose_count = 1
            else:
                lose_count = games_count[2] + 1
        update_table_liderboard_tictac(chat_id, username, first_name, \
                    last_name, 'lose_count', lose_count)
        return ConversationHandler.END

    context.bot.edit_message_text(text='Your turn', chat_id=chat_id, 
                message_id=query.message.message_id,
                reply_markup=keyboard)
    return 'GAME'


def liderboard_tictac(update, context):
    # get data from db
    top10 = get_top10_liderboard_tictac()
    # top10 - list of tuples [(username, first_name, nickname, games_count,
    #                        win_count, lose_count, draw_count), (..),..]
    chat_id = update.effective_chat.id

    if top10 == None:
        text = 'There are no players yet.\nPlay and be the first!'
    else:
        n = 1
        text_lider = ''
        for i in top10:
            name = check_liderboard_name(username=i[0], first_name=i[1], nickname=i[2])
            if name == None:
                continue
            
            lose_count = i[5]
            if lose_count == None:
                lose_count = 0
            lose_text = f'{lose_count} time' if lose_count == 1 else f'{lose_count} times'

            win_count = i[4]
            if win_count == None:
                win_count = 0
            win_text = f'{win_count} time' if win_count == 1 else f'{win_count} times'

            games_count = i[3]
            if games_count == None:
                games_count = 0
            count_text = f'{games_count} time' if games_count == 1 else f'{games_count} times'
            
            text_line = f'{n}. {name} won {win_text}, lost {lose_text}, '\
                    f'played {count_text}.\n\n'
            text_lider += text_line
            if n == 5:
                break
            n += 1
        text = 'TOP PLAYERS:\n' + text_lider
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=my_keyboard())


