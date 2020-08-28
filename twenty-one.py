from random import choice

from deck import deck


# create new dict of users card
users_card = {}


# get users_card, return summ of the card
def summ_card(**users_deck):
    points = 0
    for number in users_deck.values():
        points += (number)
    return points


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
    
    for i in range(1, 3):
        card = rand_card(**deck)
        deck = del_card_from_deck(card, **deck)
        user_card = add_user_card(card)

    # print user's deck as a list
    a = []
    for j in user_card:
        a.append(j)
    print(a)


def game(card, **deck):
    newcard = rand_card(**deck)
    deck = del_card_from_deck(newcard, **deck)
    user_card = add_user_card(newcard)

    # print user's deck as a list
    a = []
    for j in user_card:
        a.append(j)
    print(a)




def check_win(summ_card):
    if summ_card == 21:
        print('Congratulation you win!')
    elif summ_card > 21:
        print('You loose')
    else:
        print('Want to get one more card?')



def add_card(**deck):
    print(deck)






if __name__ == '__main__':

    print('Game started \nYou get: ')

    card = rand_card(**deck)
    start(card, **deck)

    running = True

    while running:
        
        points = summ_card(**users_card)
        print("Your summ = ", points)

        if points == 21:
            print('Congratulation you win!')
            break
        elif points > 21:
            print('You loose')
            break
        else:
            print('Want to get one more card?')
            game(card, **deck)

