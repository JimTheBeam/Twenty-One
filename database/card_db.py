#!/usr/bin/env python3
import sqlite3

import os


def create_table(conn):
    '''create a table'''
    try:
        conn.execute('''
            CREATE TABLE Deck
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path   VARCHAR(50)  NOT NULL UNIQUE,
            telegram_id VARCHAR(150) UNIQUE,
            card_key    VARCHAR(15)  NOT NULL UNIQUE,
            points INTEGER NOT NULL CHECK(2<=points AND points<=11),
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        print('Table created successfully')
    except sqlite3.OperationalError:
        print('Table already exist')   


def get_card_key():
    '''Find cards picture in directory pictures/
    Create a list of names without .png, .jpg
    Return this list'''
    files = os.listdir('pictures/')
    a = []
    for item in files:
        i = item.split('.')
        a.append(i[0])
    return a


def get_file_path():
    '''Find cards picture in directory /pictures
    return a list of path names to pictures'''
    pic = 'pictures/'
    files = os.listdir(pic)
    b = []
    for item in files:
        b.append('database/{0}{1}'.format(pic, item))
    return b


def get_points():
    '''create a list of points'''
    c = []
    name = os.listdir('pictures/')
    for i in name:
        try:
            number = int(i[:2])
            c.append(number)
        except ValueError:
            if i.startswith('A'):
                c.append(11)
            elif i.startswith('J'):
                c.append(2)
            elif i.startswith('Q'):
                c.append(3)
            elif i.startswith('K'):
                c.append(4)
            else:
                c.append(0)
    return c


def update_table(conn, file_path, card_key, points):
    '''inserts data in db'''
    insert = (
        'INSERT INTO deck (file_path, card_key, points)'
        'VALUES (?, ?, ?)'
        )
    try:
        for i in range(len(file_path)):
            data = (file_path[i], card_key[i], points[i])
            conn.execute(insert, data)
    except sqlite3.IntegrityError:
        print('Base already exist')
    else:
        conn.commit()
        print('Database updated successfully')


def print_data(cursor):
    '''Prints all data in the TABLE deck'''
    for row in cursor.execute('SELECT * FROM deck ORDER BY id'):
        print(row)


def update_telegram_id(conn, telegram_id, file_path):
    '''update telegram_id card using card_key
    :conn: connection to database
    :telegram_id: new telegram_id
    :card_key: card we update'''
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


def get_column_file_path(cursor):
    '''get list one of file_path from database in order id 
    :cursor: object sqlite
    :return: list'''
    select = 'SELECT file_path FROM deck ORDER BY id'
    try:      
        cursor.execute(select)
        result = cursor.fetchall()
        return result
    except sqlite3.InterfaceError:
        print('Error. Wrong args')
        return None


def get_column_card_key(cursor):
    '''get list card_key from database in order id 
    :cursor: object sqlite
    :return: list'''
    select = 'SELECT card_key FROM deck ORDER BY id'
    try:      
        cursor.execute(select)
        result = cursor.fetchall()
        return result
    except sqlite3.InterfaceError:
        print('Error. Wrong args')
        return None


def get_column_points(cursor):
    '''get list points from database in order id 
    :cursor: object sqlite
    :return: list'''
    select = 'SELECT points FROM deck ORDER BY id'
    try:      
        cursor.execute(select)
        result = cursor.fetchall()
        return result
    except sqlite3.InterfaceError:
        print('Error. Wrong args')
        return None



# TODO: MAIN FUNC!
def main():
    # Creating connection:
    conn = sqlite3.connect('deck.db')
    print('Opened database successfully')

    # create object cursor:
    cursor = conn.cursor()

    # Create a table:
    create_table(conn)

    # get data for a table:
    file_path = get_file_path()
    card_key = get_card_key()
    points = get_points()

    # insert data in the table
    update_table(conn, file_path, card_key, points)

    # print data in the table:
    # print_data(cursor)


    # print new telegram_id
    # get_telegram_id(cursor, card_key)

    # FIXME: получаем список кортежей с именами карт (card_key)
    # cursor.execute('SELECT card_key FROM deck')
    # print(cursor.fetchall())


    # close connection to database:
    conn.close()    






if __name__ == "__main__":
    main()

