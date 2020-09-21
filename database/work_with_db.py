import sqlite3

import logging

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

    # try to insert data in the database
    data = (file_path, telegram_id, card_key, points)
    try:
        conn.execute(insert, data)
        logging.info(f'table merged_photo updated with new card: {card_key}')
    except sqlite3.IntegrityError:
        logging.error(f'Imposible insert into table merged_photo new card: {card_key}')
    else:
        # save the data in the db
        conn.commit()
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
        logging.error(f'Impossible to get telegram_id from merged_photo: {e}')
    data = cursor.fetchone()
    conn.close()
    return data


# TODO: эта функция должна быть в создании таблиц
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
    logging.info('Trigger created successfully')
    try:
        cursor.execute(sql)
        logging.info('Trigger for table liderboard created successfully.')
    except sqlite3.OperationalError as e:
        logging.error(f'Impossible to create a trigger: {e}')
    
    conn.commit()
    conn.close()


def update_table_liderboard(user_id, username, first_name,
                    last_name, points, card_key, games_count):
    '''inserts data in table liderboard'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    
    sql_update = '''UPDATE OR IGNORE liderboard
            SET user_id=:user_id, username=:username, first_name=:first_name,
            last_name=:last_name, points=:points, card_key=:card_key,
            games_count=:games_count;'''

    sql_insert = '''INSERT OR IGNORE INTO liderboard
            (user_id, username, first_name, 
            last_name, points, card_key, games_count) 
            VALUES (?, ?, ?, ?, ?, ?, ?)'''

    data_update = {'user_id': user_id, 
            'username': username, 
            'first_name': first_name, 
            'last_name': last_name,
            'points': points, 
            'card_key': card_key, 
            'games_count': games_count}

    data_insert = (user_id, username, first_name, last_name, 
                    points, card_key, games_count)

    try:
        cursor.execute(sql_update, data_update)
    except sqlite3.IntegrityError as e:
        logging.error(f'Impossible to update table liderboard: {e}')
    except sqlite3.OperationalError as e:
        logging.error(f'Impossible to update table liderboard. UPDATE sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()

    try:
        cursor.execute(sql_insert, data_insert)
    except sqlite3.IntegrityError as e:
        logging.error(f'Impossible to insert data into the table liderboard: {e}')
    except sqlite3.OperationalError:
        logging.error(f'Impossible to insert into table liderboard. INSERT sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()
        conn.close()
    

# TODO: НЕ НУЖНА!!!!!!!!!!!!!!!!!11
def get_games_count_liderboad(user_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = 'SELECT games_count FROM liderboard WHERE user_id=:user_id'

    try:
        cursor.execute(sql, {'user_id': user_id})
    except sqlite3.ProgrammingError as e:
        logging.error(f'Impossible to get games_count from liderboard: {e}')
    data = cursor.fetchone()
    conn.close()
    return data


# TODO: НЕ НУЖНА!!!!!!!!!!!!!!!!!11
def get_points_liderboard(user_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = 'SELECT points FROM liderboard WHERE user_id=:user_id'

    try:
        cursor.execute(sql, {'user_id': user_id})
    except sqlite3.ProgrammingError as e:
        logging.error(f'Impossible to get points from liderboard: {e}')
    data = cursor.fetchone()
    conn.close()
    return data


# TODO: it's not needed
def get_card_key_liderboard(user_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = 'SELECT card_key FROM liderboard WHERE user_id=:user_id'
    
    try:
        cursor.execute(sql, {'user_id': user_id})
    except sqlite3.ProgrammingError as e:
        logging.error(f'Impossible to get card_key from liderboard: {e}')
    data = cursor.fetchone()
    conn.close()
    return data


def get_points_and_games_count_liderboard(user_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()

    sql = 'SELECT points, games_count FROM liderboard WHERE user_id=:user_id'
    try:
        cursor.execute(sql, {'user_id': user_id})
    except sqlite3.ProgrammingError as e:
        logging.error(f'Impossible to get points and games_count from table liderboard: {e}')
    data = cursor.fetchone()
    conn.close()
    return data    


def insert_start_data_liderboard(user_id, username, first_name, last_name):
    '''first insert data about user in table liderboard'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''INSERT  INTO liderboard
            (user_id, username, first_name, last_name, points, card_key, games_count)
            VALUES(?, ?, ?, ?, ?, ?, ?)'''
    points = 1
    card_key = 'start'
    games_count = 1
    data = (user_id, username, first_name, last_name, points, card_key, games_count)
    try:
        cursor.execute(sql, data)
    # except sqlite3.IntegrityError:
    except sqlite3.ProgrammingError as e:
        logging.error(f'Impossible to insert data into the table liderboard(start_data): {e}')
    conn.commit()
    conn.close()


def update_games_count_liderboard(user_id, games_count):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''UPDATE liderboard
             SET games_count = ? 
             WHERE user_id = ?'''

    try:
        # try to update telegram_id
        cursor.execute(sql, (games_count, user_id))
        # check if telegram_id was updated
        if cursor.rowcount < 1:
            logging.warning('games_count was not updated')
        else:
            conn.commit()
    except sqlite3.IntegrityError as e:
        logging.error(f'Impossible to update games_count table liderboard: {e}')
    conn.close()


def get_top5_liderboard():
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''SELECT first_name, points, games_count
                FROM liderboard 
                ORDER BY points DESC, games_count DESC
                LIMIT 5;
                '''
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data