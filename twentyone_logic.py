from random import choice

import os

import sqlite3

# it's not needed
import shelve

# it's not needed
from ruamel.yaml import YAML

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, TelegramError

from keyboard import my_keyboard, game_keyboard

import database.work_with_db as database

from mege_images import merge_pic


# add random card in users deck. Return list of users card
def add_newcard(users_deck, deck):
    '''pick card randomly from deck and add it in users deck'''
    while True:
        #pick card randomly from deck
        card = choice(list(deck.items()))
        # check if card in users_deck:
        if card[0] in users_deck.keys():
            continue
        else:
            #add card in users_deck
            users_deck[card[0]] = card[1] 
            break
    return users_deck


# get users_deck, return summ of the card
def get_users_deck_points(users_deck):
    '''
    :users_deck: dict of users_card
    :return: int points
    '''
    points = 0
    for item in users_deck.values():
        points += item['points']
    return points







# TODO: Сделать таблицу лидеров
# liderboard
def lider(points):
    # import liderboard from shelve file
    liderboard = shelve.open('liderboard')
    
    name = input('Enter your name: ')
    liderboard[name] = str(points)

    print('liderborad')
    for item in liderboard.items():
        print(item)

    # liderboard.clear()
    liderboard.close()





# stops conversation handler and the Game
def stop(update, context):
    text = 'Game over'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END


# this func do not needed in the game
# func updates database
# TODO: удалить эту функцию и переделать логику отправки файлов
# TODO: на попытку отправки через telegram_id, если не получилось - отправка через файл
def add_telegram_id_in_sql(update, context):
    '''send photos from database file to telegram,
    get telegram_id and insert them in database'''
    # create connection to database:
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    # get file_path from database
    file_path = database.get_column_file_path(cursor)
    # send photo to user and get telegram_id
    chat_id = update.effective_chat.id
    for item in file_path:
        # send photo:
        photo = open(item[0], 'rb')
        mess = context.bot.send_photo(chat_id=chat_id, photo=photo)
        #get telegram_id:
        telegram_id = mess.photo[1].file_id
        # update telegram_id in database
        database.update_telegram_id(conn, telegram_id, item[0])


# TODO: делает список телеграм айди в колоде пользователя
def get_telegram_id_from_user_deck(users_deck):
    '''
    :users_deck: dict of users_card
    :return: list of telegram_id in users_deck
    ['telegram_id1', 'telegram_id2', ...]
    '''
    file_id = []        
    for item in users_deck.values():
        file_id.append(item['telegram_id'])
    return file_id





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



# TODO:
# TODO:
def game_logic(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    users_deck = user_data['users_deck']
    # calculate points:
    points = get_users_deck_points(users_deck)

# TODO: добавить проверку отправилась ли фотка!!! если нет, то отправлять из файла
# TODO: добавить добавление склеенной картинки в базу данных
    chat_id = update.effective_chat.id

    # create a file with merged picture:
    file_path = merge_pic(users_deck)
    photo = open(file_path, 'rb') 

    # отправляем фото пользователю:
    try:
        # send group of photo:
        message = context.bot.send_photo(chat_id=chat_id, photo=photo)
    except TelegramError:
        # send message to user that something went wrong
        text = 'Something went wrong. Try again.'
        context.bot.send_message(chat_id= chat_id, 
                    text=text, reply_markup=my_keyboard())
        print('TelegramError')
        # FIXME: НУЖНО ПОДУМАТЬ О ВОЗВРАТЕ!!!
        points = 100
        return points

    # TODO: функцию создания списка
    # TODO: что мы должны передать file_path, telegram_id, card_key, points
    # this is telegram_id
    print(message['photo'][-1]['file_id'])


    # TODO: ПЕРЕДЕЛАТЬ РЕТУРНЫ
    # check points with 21 and send message to user:
    text = text_check_points(points)
    keyboard = keyboard_check_points(points)

    # отправляем соощение пользователю:
    context.bot.send_message(chat_id=chat_id,
                text=text, reply_markup=keyboard)

    return points






















# FIXME: добавить проверку на поинты!
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
