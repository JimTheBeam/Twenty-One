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




# get random card from deck (return dict)
def rand_card(deck):
    card = choice(list(deck.items()))
    return card


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
def summ_card(users_deck):
    points = 0
    for x in users_deck.values():
        points += x
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
    '''send photos from file to telegram,
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
    file_id = []        
    for item in users_deck.values():
        file_id.append(item['telegram_id'])
    return file_id





# FIXME: сделать эту функцию, которая выдает 2 карты пользователю
def start_game(update, context):
    print('START GAME')
    # get deck from database:
    deck = database.get_deck()
    
    # cards in user's hands:
    users_deck = {}
# TODO: ИЗМЕНИТЬ ЗНАЧЕНИЕ RANGE НА 2!!!
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck) 
    # print(users_deck.values())
 
    # cards = list(users_deck.values())[0]
    # print(cards) #it's a list obj. ['1', '2']
    
    # send cards to user
    # update.message.reply_text(text='Your cards:', reply_markup=my_keyboard())

# TODO: достать значения telegram_id из users_deck и отправить карты пользователю
# TODO: сделал так чтобы отправлялась пока 1 карта
# TODO: добавить проверку отправилась ли фотка!!! если нет, то отправлять из файла
    # send picture:
    chat_id = update.effective_chat.id
    # photo = cards.get('telegram_id')
    photo = get_telegram_id_from_user_deck(users_deck)
    print('photo:')
    print(photo)
    
    # делаем список медиа с telegram_id для отправки нескольких файлов
    media = []
    for item in photo:
        media.append(InputMediaPhoto(item))

    # отправляем 1-ую фотку:
    # context.bot.send_photo(chat_id=chat_id, photo=photo[0])
    # # отправляем 2-ую фотку:
    # context.bot.send_photo(chat_id=chat_id, photo=photo[1])

    # отправляем медиа группу(несколько фоток сразу)
    try:
        context.bot.send_media_group(chat_id=chat_id, media=media)
    except TelegramError:
        print('TelegramError')
    return 'GAME'






# TODO: сделать функцию игры(но после разборок с функцией start_game)
def game(users_deck, deck):
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck) 

# FIXME: cod below is needed to fix
    while True:
        points = summ_card(users_deck)
        print("Your summ = ", points)

        if points == 21:
            print('Congratulation you win!')
            break
        elif points > 21:
            print('You loose')
            break
        else:
            print('Do you want to get one more card?')
            print('Enter 1 for YES, 2 for NO')
            answer = enter_answer()
            if answer == 1:
                users_deck = add_newcard(users_deck, deck)
                print_cards(users_deck)
                continue
            elif answer == 2:
                print_cards(users_deck)
                print('Your summ = {points}'.format(points=points))
                break
            else:
                break

    lider(points)        

