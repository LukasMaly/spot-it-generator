import glob
import math
import random

import circlify as circ
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

            # # draw a circle around the image (for debugging)
            # cir = Circle(cx, cy, r, fillColor=colors.white)
            # drawing.add(cir)

            # rotate the image by a random angle and draw it on the card
            angle = random.randint(0, 359)
            img = Image(-r, -r, 2 * r, 2 * r, images[i])
            d = Drawing(2 * r, 2 * r)
            d.rotate(angle)
            d.add(img)
            d.translate(cx * math.cos(math.radians(-angle)) - cy * math.sin(math.radians(-angle)),
                        cx * math.sin(math.radians(-angle)) + cy * math.cos(math.radians(-angle)))

            drawing.add(d)

        return drawing

    # add cards
    for i, card in enumerate(cards):
        if i != 0 and i % (rows * columns) == 0:
            c.showPage()  # add a new page
        renderPDF.draw(draw_card(card), c, x[i % columns], y[(i // columns) % rows])

    # save the canvas
    c.save()


if __name__ == '__main__':
    order = 5  # order of cards
    images = sorted(glob.glob('./images/*.png'))  # list of the images
    create_sheets(order, images)  # create the sheets with cards
