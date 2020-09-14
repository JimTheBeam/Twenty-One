from PIL import Image

import os


def merge_pic():
    path = 'database/pictures/'
    list_of_images = os.listdir(path)

    image1 = '{}{}'.format(path,list_of_images[0])
    image2 = '{}{}'.format(path,list_of_images[1])
    print(image1)

    try:
        pil_image1 = Image.open(image1)
        pil_image2 = Image.open(image2)
    except FileNotFoundError:
        print('file not found')
    images = [pil_image1, pil_image2]
    pil_image1.load()
    pil_image2.load()

    print('the size of the image:')
    print(pil_image1.format, pil_image1.size, pil_image1.mode)
    print(pil_image2.format, pil_image2.size, pil_image2.mode)


    width1, height1 = pil_image1.size 
    width2, height2 = pil_image2.size
    total_width = width1 + width2
    total_height = max(height1, height2)
    print(total_height)
    print(total_width)


    result = Image.new('RGBA', (total_width, total_height))

    y_offset = 0
    x_offset = 0
    for item in images:
        result.paste(item, (x_offset, y_offset))
        x_offset += item.size[0]

    result_path = 'database/merged_pictures/merge.png'
    result.save('database/merged_pictures/merge.png')
    return result_path



