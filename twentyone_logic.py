import os

import sqlite3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, TelegramError

from keyboard import my_keyboard, game_keyboard

import database.work_with_db as database

from mege_images import merge_pic

from users_deck_operation import add_newcard, get_users_deck_points,\
            create_card_key_from_users_deck


# TODO: Сделать таблицу лидеров
# liderboard
# def lider(points):
    # import liderboard from shelve file
    # liderboard = shelve.open('liderboard')
    
    # name = input('Enter your name: ')
    # liderboard[name] = str(points)

    # print('liderborad')
    # for item in liderboard.items():
        # print(item)

    # liderboard.clear()
    # liderboard.close()


# stops conversation handler and the Game
def stop(update, context):
    text = 'Game over'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END


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
    request = database.get_merge_telegram_id(card_key)
    print('request:')
    print(request)

    # check if there's a telegram_id in database:
    if not request:
        # create a file with merged picture:
        file_path = merge_pic(users_deck)
        photo = open(file_path, 'rb') 

        # send photo to user:
        try:
            # send photo:
            message = context.bot.send_photo(chat_id=chat_id, photo=photo)
        except TelegramError:
            # send message to user that something went wrong
            text = 'Something went wrong. Try again.'
            context.bot.send_message(chat_id= chat_id, 
                        text=text, reply_markup=my_keyboard())
            print('TelegramError')
            points = 100
            return points

        # this is telegram_id
        telegram_id = message['photo'][-1]['file_id']
        # update database, table merged_photo
        database.update_table_merged(file_path, telegram_id, card_key, points)
    else:
        print("Send with telegram_id!!!")
        # send photo with telegram_id from database
        message = context.bot.send_photo(chat_id=chat_id, photo=request[0])

    # print(message)
    print('\nchat:')
    print(message['chat'])
    # TODO: сохранение в дб
    # names = ['lex','pex','apex']
    # snames = json.dumps(names)
    # print('\njson list:')
    # print(snames)

    # check points with 21 and send message to user:
    text = text_check_points(points)
    keyboard = keyboard_check_points(points)

    # отправляем соощение пользователю:
    context.bot.send_message(chat_id=chat_id,
                text=text, reply_markup=keyboard)
    return points


def start_game(update, context):
    # get deck from database:
    # deck = database.get_deck()
    deck = database.convert_deck_in_dict(database.get_all_data())
    
    # cards in user's hands:
    users_deck = {}

    # add cards in users_deck
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck)

    # user_data is dict. It's empty here
    user_data = context.user_data
    # insert deck and users_deck in user_data
    user_data['deck'] = deck
    user_data['users_deck'] = users_deck

    # FIXME: СЮДА ВСТАВЛЯЕТСЯ ФУНКЦИЯ ГЕЙМ ЛОГИК
    points = game_logic(update, context)

    # check if points are more than 21:
    if points >= 21:
        return ConversationHandler.END
    else:
        return 'GAME'


def game(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    deck = user_data['deck']
    users_deck = user_data['users_deck']

    # add card in users_deck
    users_deck = add_newcard(users_deck, deck) 

    # FIXME: СЮДА ВСТАВЛЯЕТСЯ ФУНКЦИЯ ГЕЙМ ЛОГИК
    points = game_logic(update, context)

    # check if points are more than 21:
    if points >= 21:
        return ConversationHandler.END
    else:
        return 'GAME'
    # lider(points)        


# отрабатывает когда нажата кнопка enough
def enough(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    users_deck = user_data['users_deck']
    chat_id = update.effective_chat.id

    points = get_users_deck_points(users_deck)
    
    text = 'Game over! Your points: {}'.format(points)
    context.bot.send_message(chat_id= chat_id, 
                    text=text, reply_markup=my_keyboard())
    return ConversationHandler.END
