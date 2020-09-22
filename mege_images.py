from PIL import Image

import logging

from users_deck_operation import create_card_key_from_users_deck,\
        get_card_key_list, get_file_path_list


def merge_pic(users_deck):
    '''combine photos in users_deck into one and
    save that photo on dick 
    return: file path to merged photo or None if creation is impossible 
    '''
    # users_deck:
    # {id: {file_path: value, telegram_id: value, card_key: value, create_time: value}}
    
    # list of file_path:
    file_path = get_file_path_list(users_deck)

    # open images with Pillow:
    images = []
    for item in file_path:
        try:
            pil_image = Image.open(item)
        except FileNotFoundError:
            logging.exception(f'merge_pic. file not found: {file_path}')
            return None
        images.append(pil_image)
        pil_image.load()
        
    # get new_file width
    total_width = 0
    for item in images:
        total_width += item.size[0]

    # get new_file height
    height = []
    for item in images:
        height.append(item.size[1])
    total_height = max(height)

    # create new file:
    result = Image.new('RGBA', (total_width, total_height))

    # add images in new file
    y_offset = 0
    x_offset = 0
    for item in images:
        result.paste(item, (x_offset, y_offset))
        x_offset += item.size[0]
    
    # create name card_key
    card_key = create_card_key_from_users_deck(users_deck)

    result_path = 'database/merged_pictures/{}.png'.format(card_key)

    result.save(result_path)
    # print(result_path)

    return result_path



