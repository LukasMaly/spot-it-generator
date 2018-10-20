import glob

import labels
from reportlab.graphics import shapes

pt_to_mm = 0.352777
mm_to_pt = 1 / pt_to_mm

images = sorted(glob.glob('./images/*.png'))

specs = labels.Specification(210, 297, 2, 3, 80, 80, corner_radius=40)

def draw_label(label, width, height, obj):
    label.add(shapes.Image(20 * mm_to_pt, 20 * mm_to_pt, 40 * mm_to_pt, 40 * mm_to_pt, obj))

sheet = labels.Sheet(specs, draw_label, border=True)

sheet.add_labels(images)

sheet.save('sheets.pdf')
