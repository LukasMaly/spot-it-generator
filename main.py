import glob
import os
import random
import shutil

import circlify as circ
import labels
from PIL import Image
from reportlab.graphics import shapes

from cards import create_cards

# points to millimeters conversion
pt_to_mm = 0.352777
mm_to_pt = 1 / pt_to_mm

# diameter of card in millimeters
diameter = 80
# margin from the card's border
margin = 5

# relative sizes of images
sizes = [1, 2, 3, 4]


def create_sheets(order, images):
    """
    Creates the sheets with cards.

    :param order: number of images at each card
    :param images: list of files with images
    """

    cards, num_pictures = create_cards(order)

    specs = labels.Specification(210, 297, 2, 3, diameter, diameter, corner_radius=diameter / 2)

    if not os.path.isdir('./temp'):
        os.makedirs('./temp')

    def draw_card(label, width, height, obj):
        s = random.choices(sizes, k=len(obj))
        s = sorted(s, reverse=True)

        circles = circ.circlify(s, with_enclosure=False)

        for i, circle in zip(obj, circles):
            cx = 3 * margin + (circle.x + 1) / 2 * (diameter - 2 * margin) * mm_to_pt
            cy = 3 * margin + (circle.y + 1) / 2 * (diameter - 2 * margin) * mm_to_pt
            r = circle.r * (diameter - 2 * margin) / 2 * mm_to_pt

            img = Image.open(images[i])
            angle = random.randint(0, 359)
            img = img.rotate(angle, fillcolor=(255, 255, 255))
            path = os.path.join('./temp', os.path.splitext(os.path.split(images[i])[1])[0] + '_' + str(angle).zfill(3) + '.png')
            img.save(path)

            x = cx - r
            y = cy - r
            img = shapes.Image(x, y, 2 * r, 2 * r, path)
            label.add(img)

    sheet = labels.Sheet(specs, draw_card, border=True)

    sheet.add_labels(cards)

    sheet.save('sheets.pdf')

    shutil.rmtree('./temp')


if __name__ == '__main__':
    order = 5
    images = sorted(glob.glob('./images/*.png'))
    create_sheets(order, images)
