from random import choice

import sys

import shelve

from ruamel.yaml import YAML

# from deck import deck


# import card deck from yaml file
yaml = YAML(typ='safe')
deck2 = yaml.load(open('deck1.yml'))
deck = deck2.get('yamldeck')


# create new list of users card
users_deck = []


# get random card from deck (return dict)
def rand_card(**deck):
    card = choice(list(deck.keys()))
    return card


# check if random card is in users deck. Return True if IN
def if_card_in_udeck(card, *users_deck):
    if card in users_deck:
        return True
    else:
        return False


# add random card in users deck. Return list of users card
def add_newcard_in_udeck(*users_deck, **deck):
    users_deck = list(users_deck)
    while True:
        card = rand_card(**deck)
        if if_card_in_udeck(card, *users_deck):
            continue
        else:
            break
    users_deck.append(card)
    print('Your new card: {}'.format(card))
    return users_deck


# get users_deck, return summ of the card
def summ_card(*users_deck, **deck):
    points = 0
    for name in users_deck:
        if deck.get(name) == None:
            pass
        else:
            points += deck.get(name)
    return points


def enter_answer():
    while True:
        try:
            answer = int(input())
            if 0 < answer < 3:
                break
            else:
                print('Only 1 for YES and 2 for NO')
                continue
        except ValueError:
            print('Wrong input try one more time.')
    return answer


def print_cards(*users_deck):
    print('Your cards:')
    print(users_deck[0])


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
    


if __name__ == '__main__':

    print('Game started')
    for x in range(2):
        users_deck = add_newcard_in_udeck(*users_deck, **deck) 
    print_cards(users_deck)
    
    while True:
        points = summ_card(*users_deck, **deck)
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
                users_deck = add_newcard_in_udeck(*users_deck, **deck)
                print_cards(users_deck)
                continue
            elif answer == 2:
                print_cards(users_deck)
                print('Your summ = {points}'.format(points=points))
                break
            else:
                print('Error')
                break

    lider(points)        
    print('Game over')


