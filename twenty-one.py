from random import choice

from deck import deck


# create new dict of users card
users_card = {}


# get users_card, return summ of the card
def summ_card(**users_deck):
    print(users_deck)
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





card = rand_card(**deck)
print('рандомная карта:')
print(card)

deck = del_card_from_deck(card, **deck)
print('новая колода')
print(deck)
    



# get random card from deck (return dict)
card = choice(list(deck.items()))
# delete chosen card from deck
deck.pop(card[0])
# add card to users dict
users_card[card[0]] = card[1]










summ_card(**users_card)



#print('your cards: ', card[0])
#print('your summ is: ', card[1])