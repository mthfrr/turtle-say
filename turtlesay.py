#!/usr/bin/env python3

import svgwrite
from cairosvg import svg2png
import cairo
import logging
import svgtextbox


logging.basicConfig(level=logging.DEBUG)

SIZE = 512
IMG_SCALE = 3.5
IMG_INSERT = SIZE - 128 * IMG_SCALE

txt = "OUI OUI ALLER"

txt_box_insert = (180, 6)
txt_box_size = (SIZE - txt_box_insert[0] - 6, 250)

dwg = svgwrite.Drawing(profile='tiny', size=(SIZE, SIZE), debug=True)

# loading turtle
base_img = svgwrite.image.Image(
    "base/turtle.svg", insert=(0, 0), size=(SIZE, SIZE))
base_img.translate(0, IMG_INSERT)
base_img.scale(IMG_SCALE)
dwg.add(base_img)

rect = svgwrite.shapes.Rect(txt_box_insert, txt_box_size)
dwg.add(rect)

# fonts = "NEIL"
txt = svgtextbox.textBuilder("OUI OUI ALLER", txt_box_size[0] - 10, 75, 0.5, font="James Tan Dinawanao")
txt.center(txt_box_size[1])
txt.translate(txt_box_insert[0] + 10, txt_box_insert[1])
dwg.add(txt)

text = svgwrite.text.Text(
    txt,
    insert=(180, 230),
    stroke='none',
    fill='#900',
    font_size='90px',
    font_weight="bold",
    font_family="Arial")
#dwg.add(text)

# export as image
svg_code = dwg.tostring()
# dwg.saveas('turtle.svg')
print(svg_code)
svg2png(bytestring=svg_code, write_to='output.png')
