from random import randint, choice

from deck import deck



    
# get random card from deck
card = choice(list(deck.items()))
print(card)

# delete chosen card from deck
deck.pop(card[0])
print(deck)






