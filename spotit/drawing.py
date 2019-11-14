import glob
import math
import random

import circlify as circ
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Circle, Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import *
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .cards import create_cards


def draw_cards(diameter, fill_color=colors.white, border_width=0, border_color=colors.white):
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

def draw_cards_images(c, images, card, sizes, diameter, margin, x, y):
    """Function called to draw a card's images."""

    # randomly choose sizes of images
    s = random.choices(sizes, k=len(card))
    s = sorted(s, reverse=True)

    # create circles packed in circle
    circles = circ.circlify(s)

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

    return c

def create_sheets(filename, order, images, sizes=[1, 2, 3, 4], seed=42, page_size='A4', diameter=80, margin=5):
    """Create the PDF with cards.
    
    :param filename: filename of the PDF
    :type filename: str
    :param order: number of images at each card
    :type order: int
    :param images: list of files with images
    :type images: list
    :param sizes: relative sizes of the images, defaults to [1, 2, 3, 4]
    :type sizes: list, optional
    :param seed: seed for random generator, defaults to 42
    :type seed: int, optional
    :param page_size: size of the page, defaults to 'A4'
    :type page_size: str or tuple of ints ([mm, mm]), optional
    :param diameter: diameter of the card [mm], defaults to 80
    :type diameter: int, optional
    :param margin: margin from the card's border [mm], defaults to 5
    :type margin: int, optional
    """
    
    # seed for random generator
    random.seed(seed)

    # size of the page
    if type(page_size) == str:
        page_size = eval(page_size)
    elif type(page_size) == tuple:
        page_size = ((page_size[0] * mm, page_size[1] * mm))

    # diameter of the card
    diameter = diameter * mm

    # margin from the card's border
    margin = margin * mm

    # create the list of sets with images' numbers
    cards, num_pictures = create_cards(order)

    # specifications of the sheet
    c = canvas.Canvas(filename, pagesize=page_size)
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

    # add cards
    for i, card in enumerate(cards):
        if i != 0 and i % (rows * columns) == 0:
            c.showPage()  # add a new page
        renderPDF.draw(draw_cards(diameter, border_width=1, border_color=colors.black), c, x[i % columns], y[(i // columns) % rows])
        c = draw_cards_images(c, images, card, sizes, diameter, margin, x[i % columns], y[(i // columns) % rows])

    # save the canvas
    c.save()
