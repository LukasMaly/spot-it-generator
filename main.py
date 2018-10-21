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
# margin from the card's border in millimeters
margin = 5

# relative sizes of images
sizes = [1, 2, 3, 4]


def create_sheets(order, images):
    """
    Creates the sheets with cards.

    :param order: number of images at each card
    :param images: list of files with images
    """

    # create the list of sets with images' numbers
    cards, num_pictures = create_cards(order)

    # specifications of the sheet
    specs = labels.Specification(210, 297, 2, 3, diameter, diameter, corner_radius=diameter / 2)

    # create a temporary directory for rotated images
    if not os.path.isdir('./temp'):
        os.makedirs('./temp')

    def draw_card(label, width, height, obj):
        """Function called to draw an individual card"""

        # randomly choose sizes of images
        s = random.choices(sizes, k=len(obj))
        s = sorted(s, reverse=True)

        # create circles packed in circle
        circles = circ.circlify(s, with_enclosure=False)

        for i, circle in zip(obj, circles):
            # calculate the center and diameter of a circle
            cx = 3 * margin + (circle.x + 1) / 2 * (diameter - 2 * margin) * mm_to_pt
            cy = 3 * margin + (circle.y + 1) / 2 * (diameter - 2 * margin) * mm_to_pt
            r = circle.r * (diameter - 2 * margin) / 2 * mm_to_pt * 0.9

            # open the image, rotate it by random angle and save it to temporary directory
            img = Image.open(images[i])
            angle = random.randint(0, 359)
            img = img.rotate(angle, expand=1, fillcolor=(255, 255, 255))
            path = os.path.join('./temp', os.path.splitext(os.path.split(images[i])[1])[0] + '_' + str(angle).zfill(3) + '.png')
            img.save(path)

            # calculate the position of the image and place it on the card
            x = cx - r
            y = cy - r
            img = shapes.Image(x, y, 2 * r, 2 * r, path)
            label.add(img)

    # create the sheet according to its specifications
    sheet = labels.Sheet(specs, draw_card, border=True)

    # add cards
    sheet.add_labels(cards)

    # save the sheet as PDF
    sheet.save('sheets.pdf')

    # remove the temporary folder and its content
    shutil.rmtree('./temp')


if __name__ == '__main__':
    order = 5  # order of the game
    images = sorted(glob.glob('./images/*.png'))  # list of the images
    create_sheets(order, images)  # create the sheets with cards
