from random import choice



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
def get_users_deck_points(users_deck):
    '''
    :users_deck: dict of users_card
    :return: int points
    '''
    points = 0
    for item in users_deck.values():
        points += item['points']
    return points


def create_card_key_from_users_deck(users_deck):
    card_key = list()
    for item in users_deck.values():
        card_key.append(item['card_key'])
    card_key = '-'.join(card_key)
    return card_key



def get_file_path_list(users_deck):
    '''
    create list file_path of cards in users_deck
    '''
    file_path = []
    for item in users_deck.values():
        file_path.append(item['file_path'])
    return file_path


def get_card_key_list(users_deck):
    '''
    create list card_key of cards in users_deck
    '''
    card_key = []
    for item in users_deck.values():
        card_key.append(item['card_key'])
    return card_key
