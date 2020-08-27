from random import choice

from deck import deck


# get users_card, return summ of the card
def summ_card(**users_deck):
    print(users_deck)
    points = 0
    for number in users_deck.values():
        points += int(number)
    print('summ = ', points)

    
# get random card from deck (return dict)
card = choice(list(deck.items()))
# delete chosen card from deck
deck.pop(card[0])
# create new dict of users card
users_card = {}
# add card to users dict
users_card[card[0]] = card[1]
print(users_card)



# get random card from deck (return dict)
card = choice(list(deck.items()))
# delete chosen card from deck
deck.pop(card[0])
# add card to users dict
users_card[card[0]] = card[1]
print(users_card)





summ_card(**users_card)



#print('your cards: ', card[0])
#print('your summ is: ', card[1])