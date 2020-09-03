from random import choice

import sys

import shelve

from ruamel.yaml import YAML

# from deck import deck

# TODO: бота 


# import card deck from yaml file
yaml = YAML(typ='safe')
deck2 = yaml.load(open('deck1.yml'))
deck = deck2.get('yamldeck')
print(len(deck))

# create new list of users card
# FIXME: before here was list
users_deck = {}


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


# print cards in users_deck
def print_cards(users_deck):
    print('Your cards:')
    print(list(users_deck.keys()))


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
        users_deck = add_newcard(users_deck, deck) 
    print_cards(users_deck)

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
                print('Error')
                break

    lider(points)        
    print('Game over')


