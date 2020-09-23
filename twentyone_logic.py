import os

import sqlite3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler

from telegram import ReplyKeyboardMarkup, TelegramError

import logging

from keyboard import my_keyboard, game_keyboard

import database.work_with_db as database

from mege_images import merge_pic

from users_deck_operation import add_newcard, get_users_deck_points,\
            create_card_key_from_users_deck


def text_check_points(points):
    '''check if points higher 21
    return text for message to user'''
    if points == 21:
        text = 'Congratulation you win! Your points: {}'.format(points)
    elif points > 21:
        text = 'You loose! Your points: {}'.format(points)
    else:
        text = 'Your points: {}. Want another card?'.format(points)
    return text


def keyboard_check_points(points):
    '''check if points higher 21
    return keyboard for message to user'''
    if points >= 21:
        keyboard = my_keyboard()
    else:
        keyboard = game_keyboard()
    return keyboard


def send_data_to_liderboard_21(chat, points, card_key, user_data):
    '''add data in table liderboard_21'''
    chat_id = chat['id']

    games_count = user_data['games_count_db'] + 1
    points_db = user_data['points_db']
    
    username = chat['username']
    first_name = chat['first_name']
    last_name = chat['last_name']

    # check if points in db are higher 
    if points_db > points:
        points = points_db

    # insert new data in table liderboard_21
    database.update_table_liderboard_21(chat_id, username, first_name,
                            last_name, points, card_key, games_count)


def game_logic(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    users_deck = user_data['users_deck']
    # calculate points:
    points = get_users_deck_points(users_deck)

    chat_id = update.effective_chat.id

    # create card_key name:
    card_key = create_card_key_from_users_deck(users_deck)

    # check if database has this card_key
    telegram_id_in_db = database.get_merge_telegram_id(card_key)

    # check if there's a telegram_id in database:
    if not telegram_id_in_db:
        # create a file with merged picture:
        file_path = merge_pic(users_deck)
        # check if merge_pic
        if file_path == None:
            logging.error(f'Func merge_pic returned None! Cards: {card_key}')
            text = f"Can't send a picture. Your cards: {card_key}, Your points: {points}"
            context.bot.send_message(text=text, reply_markup=game_keyboard())
            return points
        # open file
        try:
            photo = open(file_path, 'rb') 
        except FileNotFoundError:
            logging.exception(f'game_logic. file not found: {file_path}')
            text = f"Can't send a picture. Your cards: {card_key}, Your points: {points}"
            context.bot.send_message(text=text, reply_markup=game_keyboard())
            return points

        # send photo to user:
        try:
            # send photo:
            message = context.bot.send_photo(chat_id=chat_id, photo=photo)
        except TelegramError as e:
            logging.exception(f"Merged photo wasn't send: {e}")
            # send message to user that something went wrong
            text = 'Something went wrong. Try again.'
            context.bot.send_message(chat_id= chat_id, 
                        text=text, reply_markup=my_keyboard())
            points = 100
            return points

        # this is telegram_id
        telegram_id = message['photo'][-1]['file_id']
        # update database, table merged_photo
        database.update_table_merged(file_path, telegram_id, card_key, points)
    else:
        logging.info(f'Sending photo with telegram_id: {card_key}')
        # send photo with telegram_id from database
        message = context.bot.send_photo(chat_id=chat_id, photo=telegram_id_in_db[0])

    # check points with 21 and send message to user:
    text = text_check_points(points)
    keyboard = keyboard_check_points(points)

    # send message to user:
    context.bot.send_message(chat_id=chat_id,
                text=text, reply_markup=keyboard)
    return points


def start_game(update, context):
    logging.info('game started')
    # get deck from database:
    deck = database.convert_deck_in_dict(database.get_all_data())
    
    # chat info about user
    # chat = update.message['chat']
    chat = update.message.chat


    # TODO: ПРОВЕРИТЬ РАБОТАЕТ ЛИ ЭТО
    print('update:')
    print(update)
    print(type(update))
    print()

    user = update.effective_user
    print('user: ')
    print(user)
    print()
    # cards in user's hands:
    users_deck = {}

    # get data about user from message:
    chat_id = chat['id']
    print("chat_id: ", chat_id)
    username = chat['username']
    first_name = chat['first_name']
    last_name = chat['last_name']



    username = ''
    first_name = ''



    # try to get points and games_count from liderboard_21
    data = database.get_points_and_games_count_liderboard_21(chat_id)
    # data = (points, games_count)
    if data == None:
        # insert data about new user in database liderboard_21
        database.insert_start_data_liderboard_21(chat_id, 
                username, first_name, last_name)
        points_db = 0
        games_count_db = 0
    else:
        points_db, games_count_db = data

    # user_data is dict. It's empty here
    user_data = context.user_data

    # insert points_db and games_count in user_data:
    user_data['points_db'] = points_db
    user_data['games_count_db'] = games_count_db
    
    # add cards in users_deck
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck)
    
    # insert deck and users_deck in user_data
    user_data['deck'] = deck
    user_data['users_deck'] = users_deck

    # main func of the game:
    points = game_logic(update, context)

    # check if points are more than 21:
    if points == 21:
        card_key = create_card_key_from_users_deck(users_deck)

        send_data_to_liderboard_21(chat, points, card_key, user_data)
        return ConversationHandler.END
    elif points > 21:
        # add games_count in liderboard_21
        games_count = games_count_db + 1
        database.update_games_count_liderboard_21(chat_id, games_count)
        return ConversationHandler.END
    else:
        return 'GAME'


def game(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    deck = user_data['deck']
    users_deck = user_data['users_deck']

    chat = update.message['chat']
    chat_id = chat['id']
    # add card in users_deck
    users_deck = add_newcard(users_deck, deck) 

    # main func of the game:
    points = game_logic(update, context)

    # check if points are more than 21:
    if points == 21:
        card_key = create_card_key_from_users_deck(users_deck)
        
        send_data_to_liderboard_21(chat, points, card_key, user_data)
        return ConversationHandler.END
    elif points > 21:
        games_count_db = user_data['games_count_db']
        # add games_count in liderboard_21
        games_count = games_count_db + 1
        database.update_games_count_liderboard_21(chat_id, games_count)
        return ConversationHandler.END
    else:
        return 'GAME'       


# отрабатывает когда нажата кнопка enough
def enough(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    users_deck = user_data['users_deck']
    chat_id = update.effective_chat.id

    points = get_users_deck_points(users_deck)

    chat = update.message['chat']

    text = 'Game over! Your points: {}'.format(points)
    context.bot.send_message(chat_id= chat_id, 
                    text=text, reply_markup=my_keyboard())
    
    card_key = create_card_key_from_users_deck(users_deck)
        
    send_data_to_liderboard_21(chat, points, card_key, user_data)

    return ConversationHandler.END


def liderboard(update, context):
    '''answers when button Liderboard pressed'''
    # get top 5 from database:
    top5 = database.get_top5_liderboard_21()
    # top5 - list of tuples [(first_name, points, games_count), ..]

    chat_id = update.effective_chat.id

    if top5 == None:
        text = 'There are no playes yet.\nPlay and be the first!'
    else:
        n = 1
        text_lider = ''
        for i in top5:
            first_name = i[0]
            points = i[1]
            games_count = i[2]
            text_line = f'{n}. {first_name} has {points} max points. Played {games_count} times\n'
            text_lider += text_line
            n += 1
        text = 'TOP PLAYERS:\n' + text_lider
        context.bot.send_message(chat_id=chat_id, text=text)