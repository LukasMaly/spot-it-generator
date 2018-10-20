import os

import cv2
import numpy as np

from cards import create_cards

def generate_numbered_image(number, path, height=256, width=256):

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 4
    thickness = 4
    color = (0, 0, 0)
    text_size = cv2.getTextSize(str(number), font, font_scale, thickness)
    text_width = text_size[0][0]
    text_height = text_size[0][1]
    x = int((width - text_width) / 2)
    y = int((height + text_height) / 2)

    image = np.ones((height, width, 3), np.uint8) * 255
    image = cv2.putText(image, str(number), (x, y), fontFace=font, fontScale=font_scale, 
                        color=color, thickness=thickness)
    cv2.imwrite(path, image)


if __name__ == '__main__':
    order = 7
    cards, num_pictures = create_cards(order)

    if not os.path.isdir('./images'):
        os.makedirs('./images')

    for i in range(1, num_pictures + 1):
        filename = str(i).zfill(len(str(num_pictures + 1))) + '.png'
        generate_numbered_image(i, os.path.join('./images', filename))
