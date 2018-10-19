import os

from cards import create_cards
from utilities import generate_numbered_image

if __name__ == '__main__':
    order = 11
    cards, num_pictures = create_cards(order)

    if not os.path.isdir('./images'):
        os.makedirs('./images')

    for i in range(1, num_pictures + 1):
        filename = str(i).zfill(len(str(num_pictures + 1))) + '.png'
        generate_numbered_image(i, os.path.join('./images', filename))
