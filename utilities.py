import cv2
import numpy as np


def generate_numbered_image(number, path, height=256, width=256):

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 4
    thickness = 4
    color = (0, 0, 0, 255)
    text_size = cv2.getTextSize(str(number), font, font_scale, thickness)
    text_width = text_size[0][0]
    text_height = text_size[0][1]
    x = int((width - text_width) / 2)
    y = int((height + text_height) / 2)

    image = np.zeros((height, width, 4), np.uint8)
    image = cv2.putText(image, str(number), (x, y), fontFace=font, fontScale=font_scale, 
                        color=color, thickness=thickness)
    cv2.imwrite(path, image)
