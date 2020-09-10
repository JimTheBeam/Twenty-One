from random import choice

import os

import sqlite3

import shelve

from ruamel.yaml import YAML


# FIXME: УДАЛИТЬ ПОТОМ
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, TelegramError, InputMedia, InputMediaPhoto

from keyboard import my_keyboard, game_keyboard, file_keyboard

import database.card_db as database




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


# TODO: запилить функцию получения очков из users_deck
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




# TODO: эта функция не нужна, ее можно удалить
# TODO: сделать проверку отправилась ли фотка в телегу пользователю
def try_to_send_photo(update, context):
    print('photo')
    photo_id = 'AgACAgIAAxkBAAIN0l9Y9COQs8TZlJE4QZZSq4-CrD5UAAI3rzEbUNnISrXv8Ro0jJWk4k7zly4AAwEAAwIAA3kAA_pfAAIbBA'
    chat_id = update.effective_chat.id

    # try to send photo using photo_id
    try:
        context.bot.send_photo(chat_id=chat_id,photo=photo_id)   
        print('photo was sent') 
    except TelegramError:
        print('impossible to send photo')
        # TODO: здесь нужно код для отправки из файла










# stops conversation handler and the Game
def stop(update, context):
    text = 'Game over'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END


# this func do not needed in the game
# func updates database
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


def get_media(users_deck):
    '''
    :users_deck: dict of users_card
    :return: list of InputMediaPhoto(telegram_id) in users_deck
    [InputMediaPhoto('telegram_id1'), InputMediaPhoto(''telegram_id2'), ...]
    '''
    # get list of telegram_id ['telegram_id1', 'telegram_id2',]
    photo = get_telegram_id_from_user_deck(users_deck)
    # add
    media = []
    for item in photo:
        media.append(InputMediaPhoto(item))
    return media


# FIXME: добавить проверку на поинты!
# FIXME: сделать эту функцию, которая выдает 2 карты пользователю
def start_game(update, context):
    # get deck from database:
    deck = database.get_deck()
    
    # cards in user's hands:
    users_deck = {}
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck) 

    # user_data is dict. It's empty here
    user_data = context.user_data
    # insert deck and users_deck in user_data
    user_data['deck'] = deck
    user_data['users_deck'] = users_deck

# TODO: добавить проверку отправилась ли фотка!!! если нет, то отправлять из файла
    chat_id = update.effective_chat.id

    # get media from users_deck
    media = get_media(users_deck)
    # отправляем медиа группу(несколько фоток сразу)
    try:
        # send group of photo:
        context.bot.send_media_group(chat_id=chat_id, media=media)
    except TelegramError:
        # send message to user that something went wrong
        text = 'Something went wrong. Try again.'
        context.bot.send_message(chat_id= chat_id, 
                    text=text, reply_markup=my_keyboard())
        print('TelegramError')
        return ConversationHandler.END

    # send message with new keyboard
    context.bot.send_message(chat_id= chat_id, 
                text='Want another card?', reply_markup=game_keyboard())
    return 'GAME'






# TODO: сделать функцию игры(но после разборок с функцией start_game)
def game(update, context):
    # user_data is dict
    user_data = context.user_data
    # insert deck and users_deck in user_data
    deck = user_data['deck']
    users_deck = user_data['users_deck']
    
    # add card in users_deck
    users_deck = add_newcard(users_deck, deck) 

# TODO: добавить проверку отправилась ли фотка!!! если нет, то отправлять из файла
    chat_id = update.effective_chat.id

    # get media from users_deck
    media = get_media(users_deck)

    try:
        # send group of photo:
        context.bot.send_media_group(chat_id=chat_id, media=media)
        # send message with new keyboard
        context.bot.send_message(chat_id= chat_id, 
                    text='Want another card?', reply_markup=game_keyboard())
    except TelegramError:
        # send message to user that something went wrong
        text = 'Something went wrong. Try again.'
        context.bot.send_message(chat_id= chat_id, 
                    text=text, reply_markup=my_keyboard())
        print('TelegramError')
        return ConversationHandler.END
    return 'GAME'

    # lider(points)        


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

