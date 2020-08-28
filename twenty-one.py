from random import choice

from deck import deck


# create new dict of users card
users_card = {}


# get users_card, return summ of the card
def summ_card(**users_deck):
    points = 0
    for number in users_deck.values():
        points += (number)
    print('summ = ', points)


# get random card from deck (return dict)
def rand_card(**deck):
    card = choice(list(deck.items()))
    return card
#print('рандомная карта проверка функции')
#print(rand_card(**deck))


# delete chosen card(in rand_card) from deck
def del_card_from_deck(*card, **deck):
    card = card[0]
    deck.pop(card[0])
    return deck


def add_user_card(card):
    users_card[card[0]] = card[1]
    return users_card




def start(card, **deck):
    print('Game started \nYou get: ')
    for i in range(1, 3):
        card = rand_card(**deck)
        deck = del_card_from_deck(card, **deck)
        user_card = add_user_card(card)
    user_card_view = user_card.keys()
    print(user_card_view)




card = rand_card(**deck)
#deck = del_card_from_deck(card, **deck)
#user_card = add_user_card(card)


start(card, **deck)








summ_card(**users_card)



#print('your cards: ', card[0])
#print('your summ is: ', card[1])