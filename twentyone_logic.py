from random import choice

import os

import sqlite3

import shelve

from ruamel.yaml import YAML


# FIXME: УДАЛИТЬ ПОТОМ
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
                        ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, TelegramError

from keyboard import my_keyboard, game_keyboard, file_keyboard

import database.card_db as database




# get random card from deck (return dict)
def rand_card(deck):
    card = choice(list(deck.items()))
    return card


# add random card in users deck. Return list of users card
def add_newcard(users_deck, deck):
    card = choice(list(deck.items())) #pick card randomly from deck
    del deck[card[0]] #del card from deck
    users_deck[card[0]] = card[1] #add card in users_deck
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







# FIXME: доработать функцию получения file_id
# get file_id for photo
def check_photo(update, context):
    '''get file_id of photo user sent to bot'''
    update.message.reply_text('Обрабатываю фото', reply_markup=file_keyboard())
    photo_id = update.message.photo[-1].file_id
    print(photo_id)
    
    # pass photo_id to user_data
    context.user_data['photo_id'] = [photo_id]

    update.message.reply_text('напиши название', reply_markup=file_keyboard())
    return 'File name'


# FIXME: функция, которая получает название файла и записывает в файл
# get file name from user
def file_name(update, context):
    file_name = update.message.text
    context.user_data['file_name'] = [file_name]

      
    update.message.reply_text(file_name, reply_markup=file_keyboard())

    text = 'Your file has been saved under the name {}'.format(file_name)
    update.message.reply_text(text, reply_markup=my_keyboard()) 

    # send photo to user
    chat_id = update.effective_chat.id
    photo = context.user_data['photo_id'][0]
    print(len(photo))
    context.bot.send_photo(chat_id=chat_id, photo=photo)

    return ConversationHandler.END







# stops conversation handler and the Game
def stop(update, context):
    text = 'Game over'
    update.message.reply_text(text=text, reply_markup=my_keyboard())
    return ConversationHandler.END



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







# FIXME: сделать эту функцию, которая выдает 2 карты пользователю
def start_game(update, context):
    print('START GAME')
    # import card deck from yaml file
    yaml = YAML(typ='safe')
    deck = yaml.load(open('deck1.yml'))
    deck = deck.get('yamldeck')

    
    # cards in user's hands:
    users_deck = {}

    for _ in range(2):
        users_deck = add_newcard(users_deck, deck) 
    
    cards = list(users_deck.keys())
    print(cards) #it's a list obj. ['1', '2']
    
    # send cards to user
    update.message.reply_text(text='Your cards:', reply_markup=my_keyboard())

    # send picture:
    chat_id = update.effective_chat.id
    photo = open('foto/cards.jpg', 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=photo)

    # send list of user's card
    update.message.reply_text(text=cards, reply_markup=game_keyboard())
    return 'GAME'






# TODO: сделать функцию игры(но после разборок с функцией start_game)
def game(users_deck, deck):
    for _ in range(2):
        users_deck = add_newcard(users_deck, deck) 


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

