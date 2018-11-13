import glob
import math
import random

import circlify as circ
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Circle, Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from cards import create_cards

# seed for random generator
random.seed(42)

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

    def draw_cards(fill_color=colors.white, border_width=0, border_color=colors.white):
        """Function called to draw a card's border."""

        # card's drawing
        drawing = Drawing(diameter, diameter)

        # card's border with margin
        circle = Circle(diameter / 2, diameter / 2, diameter / 2, fillColor=border_color, strokeOpacity=0)
        drawing.add(circle)

        # card's fill
        circle = Circle(diameter / 2, diameter / 2, diameter / 2 - border_width, fillColor=fill_color, strokeOpacity=0)
        drawing.add(circle)

        return drawing

    def draw_cards_images(card, x, y):
        """Function called to draw a card's images."""

        # randomly choose sizes of images
        s = random.choices(sizes, k=len(card))
        s = sorted(s, reverse=True)

        # create circles packed in circle
        circles = circ.circlify(s, with_enclosure=False)

        for i, circle in zip(card, circles):
            # calculate the center and diameter of a circle
            cx = margin + (circle.x + 1) / 2 * (diameter - 2 * margin)
            cy = margin + (circle.y + 1) / 2 * (diameter - 2 * margin)
            r = circle.r * (diameter - 2 * margin) / 2 * 0.9  # leave some space between circles

            # # draw a circle around the image
            # def draw_circles():
            #     drawing = Drawing(diameter, diameter)
            #     circle = Circle(cx, cy, r, fillColor=colors.white)
            #     drawing.add(circle)
            #     return drawing
            # renderPDF.draw(draw_circles(), c, x, y)

            # generate a random angle
            angle = random.randint(0, 359)

            c.saveState()

            # move the canvas origin to the image's position
            c.translate(x + cx, y + cy)
            # and rotate it by random angle
            c.rotate(angle)

            # draw the image
            img = ImageReader(images[i])
            width, height = img.getSize()
            phi = math.atan(height / width)
            a = 2 * r * math.cos(phi)
            b = 2 * r * math.sin(phi)
            c.drawImage(img, -a/2, -b/2, a, b, 'auto')

            c.restoreState()

    # add cards
    for i, card in enumerate(cards):
        if i != 0 and i % (rows * columns) == 0:
            c.showPage()  # add a new page
        renderPDF.draw(draw_cards(border_width=1, border_color=colors.black), c, x[i % columns], y[(i // columns) % rows])
        draw_cards_images(card, x[i % columns], y[(i // columns) % rows])

    # save the canvas
    c.save()


if __name__ == '__main__':
    order = 5  # order of cards
    images = sorted(glob.glob('./images/*.png'))  # list of the images
    create_sheets(order, images)  # create the sheets with cards
