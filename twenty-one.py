from random import choice

from deck import deck


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




def check_win(summ_card):
    if summ_card == 21:
        print('Congratulation you win!')
    elif summ_card > 21:
        print('You loose')
    else:
        print('Want to get one more card?')










if __name__ == '__main__':

    print('Game started \nYou get: ')
    users_deck = add_newcard_in_udeck(*users_deck, **deck)
    users_deck = add_newcard_in_udeck(*users_deck, **deck)  
    print(users_deck)
    

    points = summ_card(*users_deck, **deck)

    # running = True

    # while running:
        
    #     points = summ_card(*users_deck)
    #     print("Your summ = ", points)

    #     if points == 21:
    #         print('Congratulation you win!')
    #         break
    #     elif points > 21:
    #         print('You loose')
    #         break
    #     else:
    #         print('Want to get one more card?')
    #         game(card, **deck)

