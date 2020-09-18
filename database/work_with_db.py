import sqlite3

def get_all_data():
    '''Connect to database, get data and pass it further
    return list of tuple card deck
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


# TODO: записывает telegram_id в таблицу deck
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


def get_all_merged_data():
    '''Connect to database, get data and pass it further
    return list of tuple card deck
    function must be called from file: twentyone_logic.py'''
    # Creating connection:
    conn = sqlite3.connect('database/deck.db')

    # create object cursor:
    cursor = conn.cursor()
    
    # get data from database:
    sql = 'SELECT * FROM merged_photo'
    cursor.execute(sql)
    data = cursor.fetchall()
    # data - list of tuple:
    # [(id, file_path, telegram_id, card_key, create_time), (,,),(,,)]

    # close connection to database
    conn.close
    return data


# TODO: сделать функцию записи в базу данных merged_photo
# TODO: решить что передавать в функцию
def update_table_merged(file_path, telegram_id, card_key, points):
    '''inserts data in merged_photo'''
    # open connection to db:
    conn = sqlite3.connect('database/deck.db')
    # create object cursor:
    # cursor = conn.cursor()

    insert = (
        'INSERT INTO merged_photo (file_path, telegram_id, card_key, points)'
        'VALUES (?, ?, ?, ?)'
        )

    # TODO: все что ниже не допилено пока!!!!
    # try to insert data in the database
    data = (file_path, telegram_id, card_key, points)
    try:
        conn.execute(insert, data)
    except sqlite3.IntegrityError:
        print('Impossible to insert data in the table')
    else:
        # save the data in the db
        conn.commit()
        print('Database updated successfully')
        conn.close()


def get_merge_telegram_id(card_key):
    '''try to get telegram_id with card_key
    :return: None if not such card_key in database'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = 'SELECT telegram_id FROM merged_photo WHERE card_key=:card_key'
    try:
        cursor.execute(sql, {'card_key': card_key})
    except sqlite3.ProgrammingError as e:
        print('Error: ', e)
    data = cursor.fetchone()
    conn.close()
    return data


def create_trigger_liderboard():
    '''create trigger update_time in table liderboard'''
    conn = sqlite3.connect('deck.db')
    cursor = conn.cursor()
    sql = '''CREATE TRIGGER t_UpdateLastTime  
            AFTER   
            UPDATE  
            ON liderboard
            FOR EACH ROW   
            WHEN NEW.update_time <= OLD.update_time  
            BEGIN  
            update liderboard set update_time=CURRENT_TIMESTAMP where id=OLD.id;  
            END'''
    print('Trigger created successfully')
    try:
        cursor.execute(sql)
    except sqlite3.OperationalError:
        print('Impossible to create a trigger')
    
    conn.commit()
    conn.close()


