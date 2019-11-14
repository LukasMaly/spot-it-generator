import glob
import os

from spotit.utilities import generate_images
from spotit import create_sheets


filename = 'cards.pdf'  # filename of the PDF
order = 5  # number of images at each card
images_path = './images'  # path where to store generated images

# create a directory for generated images
if not os.path.isdir(images_path):
    os.makedirs(images_path)

generate_images(images_path, order=5)  # generate images with numbers
images = sorted(glob.glob(os.path.join(images_path, '*.png')))  # list of the images
create_sheets(filename, order, images)  # create the PDF with cards
