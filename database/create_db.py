import sqlite3

import os

def create_table(conn):
    '''create a table'''
    try:
        conn.execute('''
            CREATE TABLE deck
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path   VARCHAR(50)  NOT NULL UNIQUE,
            telegram_id VARCHAR(150) UNIQUE,
            card_key    VARCHAR(15)  NOT NULL UNIQUE,
            points INTEGER NOT NULL CHECK(2<=points AND points<=11),
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        print('Table created successfully')
    except sqlite3.OperationalError:
        print('Table already exist')


def update_table(conn):
    '''inserts data in db'''
    insert = (
        'INSERT INTO deck (file_path, card_key, points)'
        'VALUES (?, ?, ?)'
        )

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
            print('Impossible to insert data in the table')
        else:
            # save the data in the db
            conn.commit()
            print('Database updated successfully')


def main():
    # Creating connection:
    conn = sqlite3.connect('deck.db')
    print('Opened database successfully')

    # Create a table:
    create_table(conn)

    # insert data in the table:
    update_table(conn)

    # close connection
    conn.close()





if __name__ == "__main__":
    main()