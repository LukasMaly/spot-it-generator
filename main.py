import glob
import os
import random
import shutil

import circlify as circ
from PIL import Image as PILImage
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Circle, Drawing, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from cards import create_cards

# size of the page
page_size = A4

# diameter of the card
diameter = 80 * mm
# margin from the card's border
margin = 5 * mm

# relative sizes of the images
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
    c = canvas.Canvas('cards.pdf', pagesize=page_size)
    width, height = page_size

    # calculate the number of columns and rows
    columns = int(width // diameter)
    rows = int(height // diameter)

    # space between cards
    x_space = (width - columns * diameter) / (columns + 1)
    y_space = (height - rows * diameter) / (rows + 1)

    # positions of the cards
    x = [x_space + i * (diameter + x_space) for i in range(columns)]
    y = [y_space + i * (diameter + y_space) for i in range(rows)]
    y = y[::-1]

    # create a temporary directory for rotated images
    if not os.path.isdir('./temp'):
        os.makedirs('./temp')

    def draw_card(obj):
        """Function called to draw an individual card."""

        # card's drawing
        drawing = Drawing(diameter, diameter)

        # card's border
        circle = Circle(diameter / 2, diameter / 2, diameter / 2, fillColor=colors.white)
        drawing.add(circle)

        # randomly choose sizes of images
        s = random.choices(sizes, k=len(obj))
        s = sorted(s, reverse=True)

        # create circles packed in circle
        circles = circ.circlify(s, with_enclosure=False)

        for i, circle in zip(obj, circles):
            # calculate the center and diameter of a circle
            cx = margin + (circle.x + 1) / 2 * (diameter - 2 * margin)
            cy = margin + (circle.y + 1) / 2 * (diameter - 2 * margin)
            r = circle.r * (diameter - 2 * margin) / 2 * 0.9

            # # draw a circle around the image
            # cir = Circle(cx, cy, r, fillColor=colors.white)
            # drawing.add(cir)

            # open the image, rotate it by random angle and save it to temporary directory
            img = PILImage.open(images[i])
            angle = random.randint(0, 359)
            img = img.rotate(angle, expand=1, fillcolor=(255, 255, 255))
            path = os.path.join('./temp', os.path.splitext(os.path.split(images[i])[1])[0] + '_' + str(angle).zfill(3) + '.png')
            img.save(path)

            # calculate the position of the image and place it on the card
            x = cx - r
            y = cy - r
            img = Image(x, y, 2 * r, 2 * r, path)
            drawing.add(img)

        return drawing

    # add cards
    for i, card in enumerate(cards):
        if i != 0 and i % (rows * columns) == 0:
            c.showPage()  # add a new page
        renderPDF.draw(draw_card(card), c, x[i % columns], y[(i // columns) % rows])

    # save the canvas
    c.save()

    # remove the temporary folder and its content
    shutil.rmtree('./temp')


if __name__ == '__main__':
    order = 5  # order of cards
    images = sorted(glob.glob('./images/*.png'))  # list of the images
    create_sheets(order, images)  # create the sheets with cards
