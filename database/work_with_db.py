import sqlite3

# TODO: достает таблицу из базы и переделывает её в словарь
def get_all_data():
    '''Connect to database, get data and create card deck dictionary
    return card deck dictionary
    function must be called from file: twentyone_logic.py'''
    # Creating connection:
    conn = sqlite3.connect('database/deck.db')

    # create object cursor:
    cursor = conn.cursor()
    
    # get data from database:
    sql = 'SELECT * FROM deck'
    cursor.execute(sql)
    data = cursor.fetchall()
    # data - list of tuple:
    # [(id, file_path, telegram_id, card_key, create_time), (,,),(,,)]

    # close connection to database
    conn.close
    return data


# TODO: функция, которая конвертирует данные из базы в словарь
def convert_deck_in_dict(deck):
    # deck - list of tuple:
    # [(id, file_path, telegram_id, card_key, create_time), (,,),(,,)]
    deck_dict = {}
    # create new dict:
    # {id: {file_path: value, telegram_id: value, card_key: value, create_time: value}}
    for item in deck:
        deck_dict[item[0]] = {'file_path': item[1],
                      'telegram_id': item[2],
                      'card_key': item[3],
                      'points': item[4],
                      'create_time': item[5]}
    return deck_dict




# TODO: записывает telegram_id в таблицу
def update_telegram_id(telegram_id, file_path):
    '''update telegram_id in database
    :telegram_id: new telegram_id
    :file_path: card we update'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    data = (telegram_id, file_path)
    update = '''UPDATE deck 
                SET telegram_id = ? 
                WHERE file_path = ?'''
    try:
        # try to update telegram_id
        cursor.execute(update, data)
        # check if telegram_id was updated
        if cursor.rowcount < 1:
            print('telegram_id was not updated')
        else:
            conn.commit()
            print('telegram_id was updated') 
    except sqlite3.IntegrityError:
        print('Error Impossible to update telegram_id')
    conn.close()


# TODO: получает телеграм айди из базы
# TODO: допилить открытие и закрытие базы данных
# TODO: функция не нужна
def get_telegram_id(cursor, card_key):
    '''get telegram_id from database 
    :cursor: object sqlite
    :card_key: card_key
    :return: telegram_id'''
    select = 'SELECT telegram_id FROM deck WHERE card_key=?'
    try:
        cursor.execute(select, ([card_key]))
        new_telegram_id = cursor.fetchone()[0]
        print(new_telegram_id)
        return new_telegram_id
    except sqlite3.InterfaceError:
        print('Error. Wrong args')