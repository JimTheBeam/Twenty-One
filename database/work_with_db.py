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
    sql = 'SELECT id, file_path, card_key, points FROM deck'

    try:
        cursor.execute(sql)
    except sqlite3.ProgrammingError as e:
        logging.exception(f'Impossible to get deck from database: {e}')
    except sqlite3.OperationalError as e:
        logging.exception(f'Impossible to get deck from database: {e}')
    data = cursor.fetchall()
    # data - list of tuple:
    # [(id, file_path, card_key, points), (,,),(,,)]

    # close connection to database
    conn.close
    return data


# TODO: функция, которая конвертирует данные из базы в словарь
def convert_deck_in_dict(deck):
    # deck - list of tuple:
    # [(id, file_path, card_key, points), (,,),(,,)]
    deck_dict = {}
    # create new dict:
    # {id: {file_path: value, telegram_id: value, card_key: value, create_time: value}}
    for item in deck:
        deck_dict[item[0]] = {'file_path': item[1],
                      'card_key': item[2],
                      'points': item[3]}
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
        logging.exception(f'Imposible insert into table merged_photo new card: {card_key}')
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
        logging.exception(f'Impossible to get telegram_id from merged_photo: {e}')
    data = cursor.fetchone()
    conn.close()
    return data


# TODO: УБРАТЬ GAMES_COUNT
def update_table_liderboard_21(chat_id, username, first_name,
                    last_name, points, card_key, count, number_count):
    '''inserts data in table liderboard_21
    :count: name of column to update
    :count: can be "win_games_count", lose_games_count, below_21_games_count
    :number_count: number counts of column :count:'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql_update = f'''UPDATE OR IGNORE liderboard_21
            SET chat_id=:chat_id, username=:username, first_name=:first_name, 
            last_name=:last_name, points=:points, card_key=:card_key, 
            {count}=:{count};'''

    sql_insert = f'''INSERT OR IGNORE INTO liderboard_21
            (chat_id, username, first_name, 
            last_name, points, card_key,{count}) 
            VALUES (?, ?, ?, ?, ?, ?, ?)'''

    data_update = {'chat_id': chat_id, 
            'username': username, 
            'first_name': first_name, 
            'last_name': last_name,
            'points': points, 
            'card_key': card_key, 
            count: number_count}

    data_insert = (chat_id, username, first_name, last_name, 
                    points, card_key, number_count)

    try:
        cursor.execute(sql_update, data_update)
    except sqlite3.IntegrityError as e:
        logging.exception(f'Impossible to update table liderboard_21: {e}')
    except sqlite3.OperationalError as e:
        logging.exception(f'Impossible to update table liderboard_21. UPDATE sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()

    try:
        cursor.execute(sql_insert, data_insert)
    except sqlite3.IntegrityError as e:
        logging.exception(f'Impossible to insert data into the table liderboard_21: {e}')
    except sqlite3.OperationalError:
        logging.exception(f'Impossible to insert into table liderboard_21. INSERT sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()
        conn.close()
    

def get_points_and_games_count_liderboard_21(chat_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()

    sql = '''SELECT points, games_count, win_games_count, 
            lose_games_count, below_21_games_count 
            FROM liderboard_21 WHERE chat_id=:chat_id'''
    try:
        cursor.execute(sql, {'chat_id': chat_id})
    except sqlite3.ProgrammingError as e:
        logging.exception(f'Impossible to get points and games_count from table liderboard_21: {e}')
    data = cursor.fetchone()
    conn.close()
    return data    



def insert_start_data_liderboard_21(chat_id, username, first_name, 
                                last_name, nickname=None, points=0, games_count=0):
    '''first insert data about user in table liderboard_21'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''INSERT OR IGNORE INTO liderboard_21
            (chat_id, username, first_name, last_name, points, games_count, nickname)
            VALUES(?, ?, ?, ?, ?, ?, ?)'''

    data = (chat_id, username, first_name, last_name, points, games_count, nickname)
    try:
        cursor.execute(sql, data)
    except sqlite3.ProgrammingError:
        logging.exception(f'Impossible to insert data into the table liderboard_21(start_data): {data}')
    except sqlite3.IntegrityError:
        logging.exception(f'Impossible to insert data into the table liderboard_21(start_data): {data}')
    conn.commit()
    conn.close()


def update_games_count_liderboard_21(chat_id, games_count):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''UPDATE liderboard_21
             SET games_count = ? 
             WHERE chat_id = ?'''

    try:
        # try to update telegram_id
        cursor.execute(sql, (games_count, chat_id))
        # check if telegram_id was updated
        if cursor.rowcount < 1:
            logging.warning('games_count was not updated')
        else:
            conn.commit()
    except sqlite3.IntegrityError as e:
        logging.exception(f'Impossible to update games_count table liderboard_21: {e}')
    conn.close()


def get_top5_liderboard_21():
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''SELECT username, first_name, nickname, points, games_count, 
                win_games_count, lose_games_count, below_21_games_count
                FROM liderboard_21 
                ORDER BY points DESC, win_games_count DESC
                LIMIT 10;
                '''
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


def update_table_liderboard_tictac(chat_id, username, first_name,
                        last_name, count, number_count):
    '''inserts data in table liderboard_tictac
    :count: name of column to update
    :count: can be "win_count", lose_count, draw_count
    :number_count: number counts of column :count:'''
    conn = sqlite3.connect('database/deck.db')    
    cursor = conn.cursor()
    sql_update = f'''UPDATE OR IGNORE liderboard_tictac
                SET chat_id=:chat_id, username=:username, first_name=:first_name,
                last_name=:last_name, {count}=:{count};'''

    sql_insert = f'''INSERT OR IGNORE INTO liderboard_tictac
            (chat_id, username, first_name, last_name, {count})
            VALUES (?, ?, ?, ?, ?);'''

    data_update = {'chat_id': chat_id, 
            'username': username, 
            'first_name': first_name, 
            'last_name': last_name, 
            count: number_count}

    data_insert = (chat_id, username, first_name, last_name, 
                    number_count)

    try:
        cursor.execute(sql_update, data_update)
    except sqlite3.IntegrityError as e:
        logging.exception(f'Impossible to update table liderboard_tictac: {e}')
    except sqlite3.OperationalError as e:
        logging.exception(f'Impossible to update table liderboard_tictac. \
                            UPDATE sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()

    try:
        cursor.execute(sql_insert, data_insert)
    except sqlite3.IntegrityError as e:
        logging.exception(f'Impossible to insert data into the table liderboard_tictac: {e}')
    except sqlite3.OperationalError:
        logging.exception(f'Impossible to insert into table liderboard_tictac. \
                        INSERT sintax is wrong: {e}')
    else:
        # save the data in the db
        conn.commit()
        conn.close()


def get_games_count_liderboard_tictac(chat_id):
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()

    sql = '''SELECT games_count, win_count, 
            lose_count, draw_count 
            FROM liderboard_tictac WHERE chat_id=:chat_id'''
    try:
        cursor.execute(sql, {'chat_id': chat_id})
    except sqlite3.ProgrammingError:
        logging.exception(f'Impossible to get points and games_count \
            from table liderboard_tictac. chat_id: {chat_id}')
    data = cursor.fetchone()
    conn.close()
    return data


def insert_start_data_liderboard_tictac(chat_id, username, first_name, 
                                last_name, nickname=None, games_count=0):
    '''first insert data about user in table liderboard_tictac'''
    conn = sqlite3.connect('database/deck.db')
    cursor = conn.cursor()
    sql = '''INSERT OR IGNORE INTO liderboard_tictac
            (chat_id, username, first_name, last_name, games_count, nickname)
            VALUES(?, ?, ?, ?, ?, ?)'''

    data = (chat_id, username, first_name, last_name, games_count, nickname)
    try:
        cursor.execute(sql, data)
    except sqlite3.ProgrammingError:
        logging.exception(f'Impossible to insert data into the table \
                            liderboard_tictac(start_data): {data}')
    except sqlite3.IntegrityError:
        logging.exception(f'Impossible to insert data into the table \
                            liderboard_tictac(start_data): {data}')
    conn.commit()
    conn.close()