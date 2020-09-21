import sqlite3

import os

import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('Creating database is starting...')


def create_table_deck(conn):
    '''create a table deck'''
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS deck
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path   VARCHAR(50)  NOT NULL UNIQUE,
            telegram_id VARCHAR(150) UNIQUE,
            card_key    VARCHAR(15)  NOT NULL UNIQUE,
            points INTEGER NOT NULL CHECK(2<=points AND points<=11),
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        logging.warning('Table deck created successfully')
    except sqlite3.OperationalError:
        logging.exception('Impossible to create table deck')
    conn.commit()


def create_table_merged_photo(conn):
    '''create a table merged_photo'''
    try:
        conn.execute('''
            CREATE TABLE  IF NOT EXISTS merged_photo
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path   VARCHAR(200)  NOT NULL UNIQUE,
            telegram_id VARCHAR(150) UNIQUE,
            card_key    VARCHAR(150)  NOT NULL UNIQUE,
            points INTEGER NOT NULL CHECK(2<=points AND points<=40),
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        logging.warning('Table merged_photo created successfully')
    except sqlite3.OperationalError:
        logging.exception('Impossible to create table merged_photo')
    conn.commit()


def create_table_liderboard(conn):
    '''create a table liderboard'''
    try:
        conn.execute('''
            CREATE TABLE  IF NOT EXISTS liderboard(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(50) NOT NULL UNIQUE,
            username VARCHAR(50) NOT NULL UNIQUE,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            points INTEGER NOT NULL CHECK(points <=21),
            card_key VARCHAR(200) NOT NULL,
            games_count INTEGER NOT NULL,
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            update_time DATETIME DEFAULT CURRENT_TIMESTAMP
            );''')
        logging.warning('Table liderboard created successfully')
    except sqlite3.OperationalError:
        logging.exception('Impossible to create table liderboard')
    conn.commit()


def create_trigger_liderboard():
    '''create trigger update_time in table liderboard'''
    conn = sqlite3.connect('deck.db')
    cursor = conn.cursor()
    sql = '''CREATE TRIGGER IF NOT EXISTS t_UpdateLastTime  
            AFTER   
            UPDATE  
            ON liderboard
            FOR EACH ROW   
            WHEN NEW.update_time <= OLD.update_time  
            BEGIN  
            update liderboard set update_time=CURRENT_TIMESTAMP where id=OLD.id;  
            END'''
    try:
        cursor.execute(sql)
        logging.info('Trigger for table liderboard created successfully.')
    except sqlite3.OperationalError as e:
        logging.exception(f'Impossible to create a trigger: {e}')
    
    conn.commit()
    conn.close()


def update_table_deck(conn):
    '''inserts data in deck'''
    insert = (
        'INSERT OR REPLACE INTO deck (file_path, card_key, points)'
        'VALUES (?, ?, ?)')

    # get list of file names in the directory /pictures: 
    # ['pictures/Q spade', 'pictures/6 club', ....]
    files = os.listdir('pictures/')

    for i in files:
        # create a data insert for database:
        file_path = 'database/{}'.format(i)
        card_key = i.split('.')[0]
        card_face = i.split(' ')[0]
        try:
            points = int(card_face)
        except ValueError:
            if card_face == 'Ace':
                points = 11
            elif card_face == 'J':
                points = 2
            elif card_face == 'Q':
                points = 3
            elif card_face == 'K':
                points = 4
            else:
                points = 0

        data = (file_path, card_key, points)

        # try to insert data in the database
        try:
            conn.execute(insert, data)
        except sqlite3.IntegrityError:
            logging.exception(f'Impossible to insert {card_key} into the table deck')
        else:
            # save the data in the db
            conn.commit()
            logging.warning(f'Table deck updated successfully with {card_key}')


def main():
    # Creating connection:
    conn = sqlite3.connect('deck.db')
    logging.info('Opened database deck.db successfully')

    # Create a table deck:
    create_table_deck(conn)

    # insert data in the table deck:
    update_table_deck(conn)

    # Create a table merged_photo:
    create_table_merged_photo(conn)

    # Create a table liderboard:
    create_table_liderboard(conn)

    # close connection
    conn.close()

    # create trigger
    create_trigger_liderboard()

    logging.info('Creating database is finished')



if __name__ == "__main__":
    main()