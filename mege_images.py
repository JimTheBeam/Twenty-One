from PIL import Image

import os


def get_file_path(users_deck):
    '''
    create list file_path of cards in users_deck
    '''
    file_path = []
    for item in users_deck.values():
        file_path.append(item['file_path'])
    return file_path
    

def merge_pic(users_deck):
    print('merge_pic')
    # users_deck:
    # {id: {file_path: value, telegram_id: value, card_key: value, create_time: value}}
    
    # list of file_path:
    file_path = get_file_path(users_deck)

    # open images with Pillow:
    images = []
    for item in file_path:
        try:
            pil_image = Image.open(item)
        except FileNotFoundError:
            print('file not found')
        images.append(pil_image)
        pil_image.load()
        
    # get new_file width
    total_width = 0
    for item in images:
        total_width += item.size[0]

    print('total_width: ', total_width)

    # get new_file height
    height = []
    for item in images:
        height.append(item.size[1])
    total_height = max(height)

    print('total_height: ', total_height)

    # create new file:
    result = Image.new('RGBA', (total_width, total_height))

    # add images in new file
    y_offset = 0
    x_offset = 0
    for item in images:
        result.paste(item, (x_offset, y_offset))
        x_offset += item.size[0]

    file_name = 'merge.png'
    result_path = 'database/merged_pictures/{}'.format(file_name)
    result.save(result_path)
    print(result_path)
    return result_path



